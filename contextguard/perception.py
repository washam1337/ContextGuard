"""Detector and tracker adapters.

Project code depends only on the small dataclasses and the ``Perception`` protocol
defined here. Ultralytics is imported lazily inside the adapters, so the rest of the
package and its tests work without loading a model.

Two kinds of box are kept apart:

* ``Detection.box``: what the detector **observed** in this frame.
* ``TrackObservation.box``: the tracker's Kalman-filtered state. For a ``lost``
  track it is a **prediction** with no detection behind it.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping, Protocol, Sequence

import numpy as np

from .geometry import Box

# COCO-80 class ids used by the FYP-1 pipeline (D03, D21).
DEFAULT_CLASSES: dict[int, str] = {0: "person", 24: "backpack", 63: "laptop"}


@dataclass(frozen=True)
class Detection:
    class_id: int
    class_name: str
    confidence: float
    box: Box


@dataclass(frozen=True)
class TrackObservation:
    track_id: str
    state: str                 # "tracked" (matched this frame) or "lost" (predicted)
    box: Box                   # tracker state; a prediction when state == "lost"
    class_id: int
    class_name: str
    detection_index: int | None  # index into FramePerception.detections, or None


@dataclass(frozen=True)
class FramePerception:
    detections: Sequence[Detection]
    tracks: Sequence[TrackObservation]
    inference_ms: float | None = None


class Perception(Protocol):
    class_names: Mapping[int, str]

    def process(self, frame: np.ndarray) -> FramePerception: ...

    def describe(self) -> dict[str, Any]: ...


def format_track_id(class_name: str, number: int) -> str:
    """Anonymous, session-scoped track ID, e.g. ``person:0003``.

    It identifies a tracker track within one run only. It is not a person's identity
    and not a registered physical asset ID.
    """
    return f"{class_name}:{int(number):04d}"


def sha256_file(path: str | Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


class ClassWiseByteTrack:
    """One Ultralytics ``BYTETracker`` per class.

    ByteTrack matches boxes by IoU without regard to class, so a single tracker could
    let a person track turn into a laptop track when the boxes overlap. Separate
    trackers keep class identity fixed for each track.
    """

    def __init__(self, class_names: Mapping[int, str], config: Mapping[str, Any]):
        from ultralytics.trackers.byte_tracker import BYTETracker

        self.class_names = dict(class_names)
        self.config = dict(config)
        args = SimpleNamespace(**{k: v for k, v in self.config.items() if k != "source"})
        self.trackers = {cid: BYTETracker(args) for cid in self.class_names}

    def update(self, boxes: Any, frame: np.ndarray | None) -> list[TrackObservation]:
        """``boxes``: NumPy-backed Ultralytics ``Boxes`` for this frame (may be empty)."""
        out: list[TrackObservation] = []
        cls = np.asarray(boxes.cls).astype(int) if len(boxes) else np.zeros(0, dtype=int)
        for cid, tracker in self.trackers.items():
            mask = cls == cid
            subset_index = np.flatnonzero(mask)
            tracker.update(boxes[mask] if len(boxes) else boxes, frame)
            fid = tracker.frame_id
            name = self.class_names[cid]
            for t in tracker.tracked_stracks:
                if not t.is_activated:
                    continue
                idx = None
                if t.frame_id == fid and t.idx is not None and 0 <= int(t.idx) < len(subset_index):
                    idx = int(subset_index[int(t.idx)])
                out.append(TrackObservation(format_track_id(name, t.track_id), "tracked",
                                            _box(t.xyxy), cid, name, idx))
            for t in tracker.lost_stracks:
                out.append(TrackObservation(format_track_id(name, t.track_id), "lost",
                                            _box(t.xyxy), cid, name, None))
        return out


def _box(values: Any) -> Box:
    x1, y1, x2, y2 = (float(v) for v in list(values)[:4])
    return (x1, y1, x2, y2)


@dataclass
class YoloByteTrackPerception:
    """Pretrained Ultralytics YOLO detector + class-wise ByteTrack, CPU by default."""

    weights: str | Path
    tracker_config: Mapping[str, Any]
    imgsz: int = 640
    conf: float = 0.10
    iou: float = 0.7
    classes: Mapping[int, str] = field(default_factory=lambda: dict(DEFAULT_CLASSES))
    device: str = "cpu"

    def __post_init__(self) -> None:
        import time

        from ultralytics import YOLO

        self._time = time
        self.weights = Path(self.weights)
        if not self.weights.is_file():
            raise FileNotFoundError(f"Weights not found: {self.weights}")
        self.weights_sha256 = sha256_file(self.weights)
        self.model = YOLO(str(self.weights), task="detect")
        model_names = dict(self.model.names)
        for cid, name in self.classes.items():
            if model_names.get(cid) != name:
                raise ValueError(f"Model class {cid} is {model_names.get(cid)!r}, expected {name!r}.")
        self.class_names = dict(self.classes)
        self.tracker = ClassWiseByteTrack(self.class_names, self.tracker_config)

    def process(self, frame: np.ndarray) -> FramePerception:
        start = self._time.perf_counter()
        result = self.model.predict(frame, imgsz=self.imgsz, conf=self.conf, iou=self.iou,
                                    classes=list(self.class_names), device=self.device,
                                    verbose=False)[0]
        elapsed = (self._time.perf_counter() - start) * 1000.0
        boxes = result.boxes.cpu().numpy()
        detections = [
            Detection(int(c), self.class_names[int(c)], float(s), _box(b))
            for b, s, c in zip(boxes.xyxy, boxes.conf, boxes.cls)
        ]
        tracks = self.tracker.update(boxes, frame)
        return FramePerception(detections, tracks, inference_ms=elapsed)

    def describe(self) -> dict[str, Any]:
        import torch
        import ultralytics

        return {
            "name": "ultralytics-yolo+bytetrack-classwise",
            "framework": {"ultralytics": ultralytics.__version__, "torch": torch.__version__},
            "weights": {"file": self.weights.name, "sha256": self.weights_sha256,
                        "provenance": "see docs/MODELS.md"},
            "class_map": {str(k): v for k, v in self.class_names.items()},
            "detector": {"imgsz": self.imgsz, "conf": self.conf, "iou": self.iou, "device": self.device},
            "tracker": {"type": "bytetrack", "per_class": True, "config": dict(self.tracker_config)},
        }
