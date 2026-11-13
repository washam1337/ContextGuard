"""Draw observation records onto frames. Display only; it creates no new information."""

from __future__ import annotations

from typing import Any, Mapping

import cv2
import numpy as np

from .zones import ZoneConfig

COLOURS = {  # BGR
    "person": (60, 200, 60),
    "laptop": (255, 150, 30),
    "backpack": (0, 150, 255),
}
DEFAULT_COLOUR = (200, 200, 200)
PREDICTED_COLOUR = (150, 150, 150)
ZONE_COLOUR = (0, 215, 255)
FONT = cv2.FONT_HERSHEY_SIMPLEX


def _label(img: np.ndarray, text: str, x: int, y: int, colour, scale: float) -> None:
    (tw, th), base = cv2.getTextSize(text, FONT, scale, 1)
    y = max(y, th + 4)
    cv2.rectangle(img, (x, y - th - 4), (x + tw + 4, y + base - 2), colour, -1)
    cv2.putText(img, text, (x + 2, y - 2), FONT, scale, (0, 0, 0), 1, cv2.LINE_AA)


def _dashed_rect(img: np.ndarray, p1, p2, colour, dash: int = 8) -> None:
    (x1, y1), (x2, y2) = p1, p2
    for x in range(x1, x2, dash * 2):
        cv2.line(img, (x, y1), (min(x + dash, x2), y1), colour, 1)
        cv2.line(img, (x, y2), (min(x + dash, x2), y2), colour, 1)
    for y in range(y1, y2, dash * 2):
        cv2.line(img, (x1, y), (x1, min(y + dash, y2)), colour, 1)
        cv2.line(img, (x2, y), (x2, min(y + dash, y2)), colour, 1)


def draw(frame: np.ndarray, record: Mapping[str, Any], zones: ZoneConfig | None) -> np.ndarray:
    img = frame.copy()
    h, w = img.shape[:2]
    scale = max(0.4, min(1.0, w / 1600))
    thick = max(1, int(round(w / 640)))
    counts = record["counts"]

    if zones:
        overlay = img.copy()
        for z in zones.zones:
            pts = np.array([[int(round(x)), int(round(y))] for x, y in z.polygon], np.int32)
            cv2.fillPoly(overlay, [pts], ZONE_COLOUR)
        cv2.addWeighted(overlay, 0.12, img, 0.88, 0, img)
        for z in zones.zones:
            pts = np.array([[int(round(x)), int(round(y))] for x, y in z.polygon], np.int32)
            cv2.polylines(img, [pts], True, ZONE_COLOUR, thick)
            zc = counts["per_zone"].get(z.id, {})
            summary = ", ".join(f"{k} {v}" for k, v in zc.items() if v)
            _label(img, f"{z.id}" + (f": {summary}" if summary else ""), int(pts[:, 0].min()),
                   int(pts[:, 1].min()) + 2, ZONE_COLOUR, scale * 0.8)

    for obj in record["objects"]:
        if obj["box_source"] == "predicted":
            x1, y1, x2, y2 = (int(round(v)) for v in obj["bbox_track"])
            _dashed_rect(img, (x1, y1), (x2, y2), PREDICTED_COLOUR)
            _label(img, f"{obj['track_id']} lost (predicted)", x1, y1, PREDICTED_COLOUR, scale * 0.7)
            continue
        colour = COLOURS.get(obj["class_name"], DEFAULT_COLOUR)
        below = obj["confidence"] < counts["count_conf"]
        x1, y1, x2, y2 = (int(round(v)) for v in obj["bbox_observed"])
        cv2.rectangle(img, (x1, y1), (x2, y2), colour, 1 if below else thick)
        name = obj["track_id"] or f"{obj['class_name']} (untracked)"
        suffix = " (below count threshold)" if below else ""
        _label(img, f"{name} {obj['confidence']:.2f}{suffix}", x1, y1, colour, scale * 0.7)

    ts = record["timestamp"]["estimated_seconds"]
    lines = [
        f"frame {record['source_frame_index']}" + (f"  ~{ts:.2f}s (est.)" if ts is not None else "  time unknown"),
        "visible: " + ", ".join(f"{k} {v}" for k, v in counts["visible_by_class"].items()),
        "inferred occupancy: not available",
    ]
    pad = 6
    line_h = int(22 * scale) + 6
    box_w = max(cv2.getTextSize(t, FONT, scale * 0.8, 1)[0][0] for t in lines) + 2 * pad
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (box_w, line_h * len(lines) + pad), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.55, img, 0.45, 0, img)
    for i, t in enumerate(lines):
        cv2.putText(img, t, (pad, (i + 1) * line_h), FONT, scale * 0.8, (255, 255, 255), 1, cv2.LINE_AA)
    return img
