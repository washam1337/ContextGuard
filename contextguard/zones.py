"""Manually configured, versioned polygon zones (schema ``contextguard.zones.v1``).

Zone membership is an observation ("the anchor point of this box lies inside the
polygon"). It is never by itself a policy violation or an anomaly.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Mapping

from .geometry import ANCHORS, Box, anchor_point, point_in_polygon

ZONES_SCHEMA = "contextguard.zones.v1"
ZONE_KINDS = ("entry", "asset_area", "restricted", "general")
BOUNDARY_POLICY = "inclusive"
ASPECT_TOLERANCE = 0.01


class ZoneConfigError(ValueError):
    """A zone configuration is malformed or unusable."""


@dataclass(frozen=True)
class Zone:
    id: str
    label: str
    kind: str
    polygon: tuple[tuple[float, float], ...]


@dataclass(frozen=True)
class ZoneConfig:
    config_id: str
    reference_width: int
    reference_height: int
    anchors: Mapping[str, str]
    zones: tuple[Zone, ...]
    draft: bool = False
    sha256: str | None = None
    path: str | None = None
    scale: tuple[float, float] = (1.0, 1.0)
    boundary_policy: str = BOUNDARY_POLICY
    notes: str = ""
    extra: Mapping[str, Any] = field(default_factory=dict)

    @property
    def zone_ids(self) -> list[str]:
        return [z.id for z in self.zones]

    def anchor_for(self, class_name: str) -> str:
        return self.anchors.get(class_name, self.anchors["default"])

    def zones_for_box(self, box: Box, class_name: str) -> list[str]:
        point = anchor_point(box, self.anchor_for(class_name))
        return [z.id for z in self.zones if point_in_polygon(point, z.polygon)]

    def scaled_for(self, width: int, height: int) -> tuple["ZoneConfig", list[str]]:
        """Scale polygons from the reference size to an actual frame size."""
        warnings: list[str] = []
        sx = width / self.reference_width
        sy = height / self.reference_height
        if abs(sx - sy) > ASPECT_TOLERANCE * max(sx, sy):
            warnings.append(
                f"Zone reference size {self.reference_width}x{self.reference_height} has a different "
                f"aspect ratio from the video frames {width}x{height}; zones may be misplaced."
            )
        if sx == 1.0 and sy == 1.0:
            return self, warnings
        zones = tuple(
            replace(z, polygon=tuple((x * sx, y * sy) for x, y in z.polygon)) for z in self.zones
        )
        return replace(self, zones=zones, scale=(sx, sy)), warnings

    def describe(self) -> dict[str, Any]:
        return {
            "schema_version": ZONES_SCHEMA,
            "config_id": self.config_id,
            "path": self.path,
            "sha256": self.sha256,
            "draft": self.draft,
            "reference_size": [self.reference_width, self.reference_height],
            "applied_scale": list(self.scale),
            "membership_anchors": dict(self.anchors),
            "boundary_policy": self.boundary_policy,
            "overlap_policy": "a box may belong to several zones at once",
            "zones": [{"id": z.id, "label": z.label, "kind": z.kind,
                       "polygon": [list(p) for p in z.polygon]} for z in self.zones],
        }


def _number(value: Any, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ZoneConfigError(f"{what} must be a number, got {value!r}.")
    return float(value)


def parse_zone_config(data: Any, sha256: str | None = None, path: str | None = None) -> ZoneConfig:
    if not isinstance(data, dict):
        raise ZoneConfigError("Zone configuration must be a JSON object.")
    if data.get("schema_version") != ZONES_SCHEMA:
        raise ZoneConfigError(f"schema_version must be {ZONES_SCHEMA!r}, got {data.get('schema_version')!r}.")
    config_id = data.get("config_id")
    if not isinstance(config_id, str) or not config_id.strip():
        raise ZoneConfigError("config_id must be a non-empty string.")
    width, height = data.get("reference_width"), data.get("reference_height")
    for name, value in (("reference_width", width), ("reference_height", height)):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ZoneConfigError(f"{name} must be a positive integer.")
    if data.get("boundary_policy", BOUNDARY_POLICY) != BOUNDARY_POLICY:
        raise ZoneConfigError(f"Only boundary_policy {BOUNDARY_POLICY!r} is supported.")

    anchors = dict(data.get("membership_anchors", {}))
    anchors.setdefault("default", "center")
    for cls, anchor in anchors.items():
        if anchor not in ANCHORS:
            raise ZoneConfigError(f"Anchor for {cls!r} must be one of {ANCHORS}, got {anchor!r}.")

    raw_zones = data.get("zones")
    if not isinstance(raw_zones, list) or not raw_zones:
        raise ZoneConfigError("zones must be a non-empty list.")
    zones: list[Zone] = []
    seen: set[str] = set()
    for i, raw in enumerate(raw_zones):
        if not isinstance(raw, dict):
            raise ZoneConfigError(f"Zone {i} must be an object.")
        zid = raw.get("id")
        if not isinstance(zid, str) or not zid.strip():
            raise ZoneConfigError(f"Zone {i} needs a non-empty string id.")
        if zid in seen:
            raise ZoneConfigError(f"Duplicate zone id {zid!r}.")
        seen.add(zid)
        kind = raw.get("kind", "general")
        if kind not in ZONE_KINDS:
            raise ZoneConfigError(f"Zone {zid!r} kind must be one of {ZONE_KINDS}, got {kind!r}.")
        polygon = raw.get("polygon")
        if not isinstance(polygon, list) or len(polygon) < 3:
            raise ZoneConfigError(f"Zone {zid!r} polygon needs at least 3 points.")
        points = []
        for j, pt in enumerate(polygon):
            if not isinstance(pt, list) or len(pt) != 2:
                raise ZoneConfigError(f"Zone {zid!r} point {j} must be [x, y].")
            x = _number(pt[0], f"Zone {zid!r} point {j} x")
            y = _number(pt[1], f"Zone {zid!r} point {j} y")
            if not (0 <= x <= width and 0 <= y <= height):
                raise ZoneConfigError(f"Zone {zid!r} point {j} ({x}, {y}) lies outside the reference image.")
            points.append((x, y))
        zones.append(Zone(zid, str(raw.get("label", zid)), kind, tuple(points)))

    return ZoneConfig(
        config_id=config_id, reference_width=width, reference_height=height,
        anchors=anchors, zones=tuple(zones), draft=bool(data.get("draft", False)),
        sha256=sha256, path=path, notes=str(data.get("notes", "")),
    )


def load_zone_config(path: str | Path) -> ZoneConfig:
    p = Path(path)
    raw = p.read_bytes()
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ZoneConfigError(f"Cannot parse zone configuration {p}: {exc}") from exc
    return parse_zone_config(data, sha256=hashlib.sha256(raw).hexdigest(), path=str(p))
