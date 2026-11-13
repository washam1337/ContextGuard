"""Frame-level observation records (schema ``contextguard.observation.v1``).

This schema is separate from the CG-002 inspection schema and from any later
event/incident schema. It records **observations** only.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from .perception import FramePerception
from .zones import ZoneConfig

OBSERVATION_SCHEMA = "contextguard.observation.v1"
COUNT_POLICY = "contextguard.count_policy.v1"
TIMING_BASIS = "source_frame_index / reported_fps (assumes constant frame rate)"
BBOX_CONVENTION = "xyxy, float pixels, origin top-left, x right, y down"
TRACK_STATES = ("tracked", "untracked", "lost")
BOX_SOURCES = ("observed", "predicted")

COUNT_POLICY_DESCRIPTION = (
    "Visible counts include only boxes the detector observed in this frame "
    "(box_source == 'observed') with confidence >= count_conf, whatever their track "
    "state. Tracker predictions for lost tracks are never counted. A box is counted in "
    "every zone that contains its membership anchor point. Visible counts are not "
    "inferred room occupancy and not cumulative arrivals."
)

INFERRED_OCCUPANCY_UNAVAILABLE = {
    "value": None,
    "available": False,
    "method": None,
    "reason": "Occupancy inference is not implemented in the FYP-1 perception pipeline; "
              "visible counts must not be substituted for it.",
}


class ObservationSchemaError(ValueError):
    """A record does not satisfy contextguard.observation.v1."""


def _r(box) -> list[float]:
    return [round(float(v), 2) for v in box]


def build_objects(perception: FramePerception, zones: ZoneConfig | None) -> list[dict[str, Any]]:
    """Merge detector output and tracker state into one list of object entries."""
    matched: dict[int, Any] = {}
    for t in perception.tracks:
        if t.state == "tracked" and t.detection_index is not None:
            matched[t.detection_index] = t
    objects: list[dict[str, Any]] = []
    for i, det in enumerate(perception.detections):
        track = matched.get(i)
        objects.append({
            "class_id": det.class_id,
            "class_name": det.class_name,
            "confidence": round(det.confidence, 4),
            "box_source": "observed",
            "bbox_observed": _r(det.box),
            "bbox_track": _r(track.box) if track else None,
            "track_id": track.track_id if track else None,
            "track_state": "tracked" if track else "untracked",
            "zones": zones.zones_for_box(det.box, det.class_name) if zones else [],
        })
    for t in perception.tracks:
        if t.state == "lost":
            objects.append({
                "class_id": t.class_id,
                "class_name": t.class_name,
                "confidence": None,
                "box_source": "predicted",
                "bbox_observed": None,
                "bbox_track": _r(t.box),
                "track_id": t.track_id,
                "track_state": "lost",
                "zones": zones.zones_for_box(t.box, t.class_name) if zones else [],
            })
    return objects


def compute_counts(objects: Iterable[Mapping[str, Any]], class_names: Iterable[str],
                   zone_ids: Iterable[str], count_conf: float) -> dict[str, Any]:
    names = list(class_names)
    by_class = {n: 0 for n in names}
    per_zone = {z: {n: 0 for n in names} for z in zone_ids}
    for obj in objects:
        if obj["box_source"] != "observed" or obj["confidence"] is None:
            continue
        if obj["confidence"] < count_conf:
            continue
        name = obj["class_name"]
        if name not in by_class:
            continue
        by_class[name] += 1
        for z in obj["zones"]:
            if z in per_zone:
                per_zone[z][name] += 1
    return {
        "policy": COUNT_POLICY,
        "count_conf": count_conf,
        "visible_persons": by_class.get("person", 0),
        "visible_by_class": by_class,
        "per_zone": per_zone,
    }


def build_frame_record(*, run_id: str, source_frame_index: int, processed_index: int,
                       annotated_frame_index: int | None, width: int, height: int,
                       estimated_seconds: float | None, decoder_pos_msec: float | None,
                       objects: list[dict[str, Any]], counts: dict[str, Any],
                       warnings: list[str] | None = None) -> dict[str, Any]:
    return {
        "schema_version": OBSERVATION_SCHEMA,
        "run_id": run_id,
        "source_frame_index": source_frame_index,
        "processed_index": processed_index,
        "annotated_frame_index": annotated_frame_index,
        "frame_width": width,
        "frame_height": height,
        "timestamp": {
            "estimated_seconds": None if estimated_seconds is None else round(estimated_seconds, 4),
            "basis": TIMING_BASIS,
            "decoder_pos_msec": None if decoder_pos_msec is None else round(decoder_pos_msec, 3),
            "validated": False,
        },
        "objects": objects,
        "counts": counts,
        "inferred_occupancy": dict(INFERRED_OCCUPANCY_UNAVAILABLE),
        "warnings": list(warnings or []),
    }


def _fail(msg: str) -> None:
    raise ObservationSchemaError(msg)


def _is_box(v: Any) -> bool:
    return (isinstance(v, list) and len(v) == 4
            and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v)
            and v[0] <= v[2] and v[1] <= v[3])


def _nonneg_int(v: Any) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def validate_observation(rec: Mapping[str, Any]) -> None:
    """Raise ObservationSchemaError unless ``rec`` is a valid v1 record."""
    required = ("schema_version", "run_id", "source_frame_index", "processed_index",
                "annotated_frame_index", "frame_width", "frame_height", "timestamp",
                "objects", "counts", "inferred_occupancy", "warnings")
    for key in required:
        if key not in rec:
            _fail(f"missing key {key!r}")
    if rec["schema_version"] != OBSERVATION_SCHEMA:
        _fail("wrong schema_version")
    if not isinstance(rec["run_id"], str) or not rec["run_id"]:
        _fail("run_id must be a non-empty string")
    for key in ("source_frame_index", "processed_index", "frame_width", "frame_height"):
        if not _nonneg_int(rec[key]):
            _fail(f"{key} must be a non-negative integer")
    if rec["annotated_frame_index"] is not None and not _nonneg_int(rec["annotated_frame_index"]):
        _fail("annotated_frame_index must be null or a non-negative integer")
    ts = rec["timestamp"]
    if not isinstance(ts, dict) or ts.get("basis") != TIMING_BASIS or ts.get("validated") is not False:
        _fail("timestamp must state the timing basis and validated=false")
    if ts.get("estimated_seconds") is not None and not isinstance(ts["estimated_seconds"], (int, float)):
        _fail("estimated_seconds must be a number or null")
    if not isinstance(rec["objects"], list):
        _fail("objects must be a list")
    for i, o in enumerate(rec["objects"]):
        where = f"objects[{i}]"
        if o.get("box_source") not in BOX_SOURCES:
            _fail(f"{where}.box_source invalid")
        if o.get("track_state") not in TRACK_STATES:
            _fail(f"{where}.track_state invalid")
        if not isinstance(o.get("class_name"), str) or not _nonneg_int(o.get("class_id")):
            _fail(f"{where} needs class_id and class_name")
        if not isinstance(o.get("zones"), list):
            _fail(f"{where}.zones must be a list")
        if o["box_source"] == "observed":
            if not _is_box(o.get("bbox_observed")):
                _fail(f"{where}: observed object needs bbox_observed")
            if not isinstance(o.get("confidence"), (int, float)) or not 0 <= o["confidence"] <= 1:
                _fail(f"{where}: observed object needs confidence in [0, 1]")
            if o["track_state"] == "lost":
                _fail(f"{where}: an observed box cannot be in state 'lost'")
            if o["track_state"] == "tracked" and (o.get("track_id") is None or not _is_box(o.get("bbox_track"))):
                _fail(f"{where}: tracked object needs track_id and bbox_track")
            if o["track_state"] == "untracked" and (o.get("track_id") is not None or o.get("bbox_track") is not None):
                _fail(f"{where}: untracked object must have no track_id/bbox_track")
        else:
            if o.get("bbox_observed") is not None or o.get("confidence") is not None:
                _fail(f"{where}: predicted object must have no observed box or detector confidence")
            if o["track_state"] != "lost" or o.get("track_id") is None or not _is_box(o.get("bbox_track")):
                _fail(f"{where}: predicted object must be a lost track with bbox_track")
    counts = rec["counts"]
    if not isinstance(counts, dict) or counts.get("policy") != COUNT_POLICY:
        _fail("counts must declare the count policy")
    if not _nonneg_int(counts.get("visible_persons")):
        _fail("visible_persons must be a non-negative integer")
    occ = rec["inferred_occupancy"]
    if not isinstance(occ, dict) or "value" not in occ or "available" not in occ:
        _fail("inferred_occupancy must have value and available")
    if occ["available"] is False and occ["value"] is not None:
        _fail("unavailable inferred occupancy must be null, not a number")
    if not isinstance(rec["warnings"], list):
        _fail("warnings must be a list")
