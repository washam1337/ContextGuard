"""Sequential video decoding with explicit timing, and annotated-video writing."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import cv2
import numpy as np

# Annotated-output codecs verified to write and read back with this OpenCV build
# (2026-11-13). H.264 is not available without an external FFmpeg.
CODECS = {"mp4v": ".mp4", "MJPG": ".avi", "VP80": ".webm"}


class VideoError(RuntimeError):
    """The source cannot be decoded or the output cannot be written."""


def _positive(value: float) -> float | None:
    return value if math.isfinite(value) and value > 0 else None


@dataclass(frozen=True)
class SourceMetadata:
    reported_fps: float | None
    reported_frame_count: int | None
    reported_width: int | None
    reported_height: int | None
    backend: str


@dataclass(frozen=True)
class DecodedFrame:
    index: int                      # zero-based decoded index in the source
    decoder_pos_msec: float | None  # as reported by the backend; NOT validated
    image: np.ndarray


class FrameSource:
    """Iterate decoded frames in order, never seeking. Stops at the first read failure."""

    def __init__(self, path: str | Path):
        self.path = str(path)
        self.capture = cv2.VideoCapture(self.path)
        if not self.capture.isOpened():
            raise VideoError("Cannot open video: unreadable content, unsupported codec, or damaged input.")
        fps = _positive(float(self.capture.get(cv2.CAP_PROP_FPS)))
        count = _positive(float(self.capture.get(cv2.CAP_PROP_FRAME_COUNT)))
        w = _positive(float(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
        h = _positive(float(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.metadata = SourceMetadata(
            reported_fps=fps,
            reported_frame_count=int(count) if count and count.is_integer() else None,
            reported_width=int(w) if w else None,
            reported_height=int(h) if h else None,
            backend=self.capture.getBackendName(),
        )
        self.stop_reason: str | None = None
        self.warnings: list[str] = []
        if fps is None:
            self.warnings.append("Reported FPS is invalid or unavailable; estimated timestamps are null.")

    def __iter__(self) -> Iterator[DecodedFrame]:
        index = 0
        while True:
            try:
                ok, frame = self.capture.read()
            except cv2.error:
                self.stop_reason = "decoder_exception"
                self.warnings.append("OpenCV raised a decoding error; only the decoded prefix was processed.")
                return
            if not ok:
                self.stop_reason = "read_returned_false"
                return
            if frame is None or frame.size == 0:
                self.stop_reason = "empty_frame"
                self.warnings.append("Decoder returned an empty frame; processing stopped.")
                return
            pos = _positive(float(self.capture.get(cv2.CAP_PROP_POS_MSEC)))
            yield DecodedFrame(index, pos if pos is not None else (0.0 if index == 0 else None), frame)
            index += 1

    def estimated_seconds(self, index: int) -> float | None:
        fps = self.metadata.reported_fps
        return index / fps if fps else None

    def close(self) -> None:
        self.capture.release()

    def __enter__(self) -> "FrameSource":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


class AnnotatedVideoWriter:
    """Opens lazily on the first frame, so the output size always matches the frames."""

    def __init__(self, path: str | Path, fps: float, codec: str = "mp4v"):
        if codec not in CODECS:
            raise VideoError(f"Unsupported codec {codec!r}; choose one of {sorted(CODECS)}.")
        self.path = Path(path)
        self.fps = fps
        self.codec = codec
        self.writer: cv2.VideoWriter | None = None
        self.frames_written = 0
        self.size: tuple[int, int] | None = None

    def write(self, image: np.ndarray) -> int:
        h, w = image.shape[:2]
        if self.writer is None:
            if self.path.exists():
                raise VideoError(f"Refusing to overwrite {self.path}.")
            self.writer = cv2.VideoWriter(str(self.path), cv2.VideoWriter_fourcc(*self.codec), self.fps, (w, h))
            if not self.writer.isOpened():
                raise VideoError(f"Cannot open video writer for codec {self.codec}.")
            self.size = (w, h)
        elif (w, h) != self.size:
            image = cv2.resize(image, self.size)
        self.writer.write(image)
        self.frames_written += 1
        return self.frames_written - 1

    def close(self) -> None:
        if self.writer is not None:
            self.writer.release()
