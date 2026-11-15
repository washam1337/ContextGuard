"""Recorded video → detection → tracking → zones/counting → annotated video + JSONL.

Outputs (in a new directory that must not already exist):

* ``observations.jsonl``: one ``contextguard.observation.v1`` record per processed
  frame, including frames with no detections.
* ``annotated.<ext>``: one annotated frame per processed frame, in the same order.
  ``annotated_frame_index`` in each record gives the matching video frame.
* ``manifest.json``: ``contextguard.run_manifest.v1`` provenance and run summary.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
import uuid
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

import cv2
import numpy as np

from . import __version__
from .annotate import draw
from .observation import (BBOX_CONVENTION, COUNT_POLICY, COUNT_POLICY_DESCRIPTION, OBSERVATION_SCHEMA,
                          TIMING_BASIS, build_frame_record, build_objects, compute_counts,
                          validate_observation)
from .perception import DEFAULT_CLASSES, Perception, sha256_file
from .video import CODECS, AnnotatedVideoWriter, FrameSource, VideoError
from .zones import ZoneConfig, load_zone_config

MANIFEST_SCHEMA = "contextguard.run_manifest.v1"
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACKER_CONFIG = REPO_ROOT / "configs" / "tracker" / "bytetrack.json"


class PipelineError(RuntimeError):
    """Input, configuration or output problem that stops a run."""


@dataclass
class PipelineConfig:
    input: Path
    output: Path
    weights: Path | None = None
    zones: Path | None = None
    tracker_config: Path = DEFAULT_TRACKER_CONFIG
    imgsz: int = 640
    conf: float = 0.10          # detector threshold (feeds ByteTrack's low-score stage)
    count_conf: float = 0.25    # threshold for visible counts
    iou: float = 0.7
    stride: int = 1
    max_frames: int | None = None
    write_video: bool = True
    codec: str = "mp4v"
    threads: int | None = None
    classes: Mapping[int, str] = field(default_factory=lambda: dict(DEFAULT_CLASSES))
    argv: list[str] | None = None


def load_tracker_config(path: Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {"tracker_type", "track_high_thresh", "track_low_thresh", "new_track_thresh",
                "track_buffer", "match_thresh", "fuse_score"}
    missing = required - data.keys()
    if missing or data.get("tracker_type") != "bytetrack":
        raise PipelineError(f"Tracker config {path} must be a bytetrack config; missing {sorted(missing)}.")
    return data


def _git_revision() -> dict[str, Any]:
    try:
        rev = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True,
                             text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=REPO_ROOT,
                               capture_output=True, text=True, check=True).stdout.strip() != ""
        return {"commit": rev, "uncommitted_changes": dirty}
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "uncommitted_changes": None}


def _hardware() -> dict[str, Any]:
    cpu = None
    mem_gib = None
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip()
                break
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal"):
                mem_gib = round(int(line.split()[1]) / 1048576, 2)
                break
    except OSError:
        pass
    return {"cpu": cpu or platform.processor() or None, "logical_cpus": os.cpu_count(),
            "ram_gib": mem_gib, "gpu": None, "platform": platform.platform()}


def _check_paths(cfg: PipelineConfig) -> Path:
    source = Path(cfg.input).expanduser().resolve(strict=True)
    if not source.is_file():
        raise PipelineError("Input must be a local regular video file.")
    with source.open("rb"):
        pass
    if source.stat().st_size == 0:
        raise PipelineError("Input is empty (zero bytes).")
    out = Path(cfg.output).expanduser().absolute()
    if out.exists() or out.is_symlink():
        raise PipelineError("Output path already exists; choose a new directory. Nothing overwritten.")
    if cfg.stride < 1:
        raise PipelineError("stride must be >= 1.")
    if cfg.max_frames is not None and cfg.max_frames < 1:
        raise PipelineError("max_frames must be >= 1.")
    if not 0 <= cfg.conf <= cfg.count_conf <= 1:
        raise PipelineError("Require 0 <= conf <= count_conf <= 1.")
    if cfg.codec not in CODECS:
        raise PipelineError(f"codec must be one of {sorted(CODECS)}.")
    return source


def run_pipeline(cfg: PipelineConfig,
                 perception_factory: Callable[[PipelineConfig, dict[str, Any]], Perception] | None = None
                 ) -> dict[str, Any]:
    source = _check_paths(cfg)
    out = Path(cfg.output).expanduser().absolute()
    tracker_cfg = load_tracker_config(cfg.tracker_config)
    zones: ZoneConfig | None = load_zone_config(cfg.zones) if cfg.zones else None
    if cfg.threads:
        try:
            import torch
            torch.set_num_threads(cfg.threads)
        except ImportError:
            pass

    if perception_factory is None:
        if cfg.weights is None:
            raise PipelineError("--weights is required.")
        from .perception import YoloByteTrackPerception

        def perception_factory(c: PipelineConfig, tcfg: dict[str, Any]) -> Perception:
            return YoloByteTrackPerception(weights=c.weights, tracker_config=tcfg, imgsz=c.imgsz,
                                           conf=c.conf, iou=c.iou, classes=c.classes)

    source_sha = sha256_file(source)
    perception = perception_factory(cfg, tracker_cfg)
    class_names = list(perception.class_names.values())

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    warnings: list[str] = []
    status = "failed"
    stats: dict[str, Any] = {"frames_decoded": 0, "frames_processed": 0, "empty_frames": 0,
                             "observed_by_class": Counter(), "predicted_entries": 0,
                             "untracked_detections": 0, "track_ids": set(), "inference_ms": []}
    writer = None
    src = None
    error: str | None = None
    try:
        src = FrameSource(source)
        meta = src.metadata
        # Zones are scaled against the size of the *decoded* frames, never the reported
        # metadata size, which can differ (e.g. phone rotation metadata). The loaded
        # config is kept unscaled so every rescale starts from the reference size.
        base_zones = zones
        zones_frame_size: tuple[int, int] | None = None
        if zones and zones.draft:
            warnings.append(f"Zone configuration {zones.config_id!r} is marked draft.")
        if cfg.write_video:
            fps_out = (meta.reported_fps or 30.0) / cfg.stride
            if meta.reported_fps is None:
                warnings.append("Annotated video uses a nominal 30 fps because the source FPS is unknown.")
            writer = AnnotatedVideoWriter(out / f"annotated{CODECS[cfg.codec]}", fps_out, cfg.codec)
        with (out / "observations.jsonl").open("x", encoding="utf-8") as jsonl:
            for frame in src:
                stats["frames_decoded"] += 1
                if frame.index % cfg.stride:
                    continue
                if cfg.max_frames is not None and stats["frames_processed"] >= cfg.max_frames:
                    break
                h, w = frame.image.shape[:2]
                if base_zones and zones_frame_size != (w, h):
                    if zones_frame_size is None:
                        reported = (meta.reported_width, meta.reported_height)
                        if None not in reported and reported != (w, h):
                            warnings.append(
                                f"Decoded frame size {w}x{h} differs from the reported size "
                                f"{reported[0]}x{reported[1]}; zones are scaled to the decoded frames.")
                    else:
                        warnings.append(
                            f"Frame size changed from {zones_frame_size[0]}x{zones_frame_size[1]} to "
                            f"{w}x{h} at source frame {frame.index}; zones re-scaled.")
                    zones, zw = base_zones.scaled_for(w, h)
                    warnings += [x for x in zw if x not in warnings]
                    zones_frame_size = (w, h)
                result = perception.process(frame.image)
                if result.inference_ms is not None:
                    stats["inference_ms"].append(result.inference_ms)
                objects = build_objects(result, zones)
                counts = compute_counts(objects, class_names, zones.zone_ids if zones else [], cfg.count_conf)
                annotated_index = writer.frames_written if writer else None
                record = build_frame_record(
                    run_id=run_id, source_frame_index=frame.index,
                    processed_index=stats["frames_processed"], annotated_frame_index=annotated_index,
                    width=w, height=h, estimated_seconds=src.estimated_seconds(frame.index),
                    decoder_pos_msec=frame.decoder_pos_msec, objects=objects, counts=counts)
                validate_observation(record)
                jsonl.write(json.dumps(record, allow_nan=False) + "\n")
                if writer:
                    writer.write(draw(frame.image, record, zones))
                stats["frames_processed"] += 1
                if not objects:
                    stats["empty_frames"] += 1
                for o in objects:
                    if o["box_source"] == "observed":
                        stats["observed_by_class"][o["class_name"]] += 1
                        if o["track_state"] == "untracked":
                            stats["untracked_detections"] += 1
                    else:
                        stats["predicted_entries"] += 1
                    if o["track_id"]:
                        stats["track_ids"].add(o["track_id"])
        warnings += src.warnings
        if stats["frames_processed"] == 0:
            raise VideoError("No frames decoded: empty video, unsupported codec, or damaged input.")
        status = "completed"
    except Exception as exc:  # recorded in the manifest, then re-raised
        error = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        if writer:
            writer.close()
        if src:
            src.close()
        runtime = time.perf_counter() - started
        manifest = _manifest(cfg, run_id, source, source_sha, src, perception, zones, tracker_cfg,
                             stats, runtime, warnings, status, error, writer)
        with (out / "manifest.json").open("x", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, allow_nan=False)
            fh.write("\n")
    return manifest


def _manifest(cfg, run_id, source, source_sha, src, perception, zones, tracker_cfg, stats, runtime,
              warnings, status, error, writer) -> dict[str, Any]:
    inf = stats["inference_ms"]
    track_ids = sorted(stats["track_ids"])
    meta = src.metadata if src else None
    return {
        "schema_version": MANIFEST_SCHEMA,
        "run_id": run_id,
        "status": status,
        "error": error,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "command": cfg.argv,
        "code": {"package": "contextguard", "version": __version__, **_git_revision()},
        "source": {
            "path": str(source), "size_bytes": source.stat().st_size, "sha256": source_sha,
            "reported_fps": meta.reported_fps if meta else None,
            "reported_frame_count": meta.reported_frame_count if meta else None,
            "reported_size": [meta.reported_width, meta.reported_height] if meta else None,
            "decoder": {"library": "OpenCV", "version": cv2.__version__, "backend": meta.backend if meta else None},
            "stop_reason": src.stop_reason if src else None,
        },
        "processing": {"stride": cfg.stride, "max_frames": cfg.max_frames, "threads": cfg.threads,
                       "detector_conf": cfg.conf, "count_conf": cfg.count_conf},
        "perception": perception.describe(),
        "tracker_config_file": str(cfg.tracker_config),
        "zones": zones.describe() if zones else None,
        "contracts": {
            "observation_schema": OBSERVATION_SCHEMA,
            "bbox_convention": BBOX_CONVENTION,
            "timing_basis": TIMING_BASIS,
            "timestamps_validated": False,
            "count_policy": COUNT_POLICY,
            "count_policy_description": COUNT_POLICY_DESCRIPTION,
            "track_ids": "anonymous, session-scoped per run; not identities and not registered asset IDs",
            "confidence": "detector confidence; not a calibrated probability",
            "inferred_occupancy": "not implemented; always null",
        },
        "software": {"python": sys.version.split()[0], "numpy": np.__version__, "opencv": cv2.__version__},
        "hardware": _hardware(),
        "outputs": {
            "observations": "observations.jsonl",
            "annotated_video": writer.path.name if writer and writer.frames_written else None,
            "annotated_codec": cfg.codec if writer else None,
            "annotated_frames": writer.frames_written if writer else 0,
            "alignment": "annotated frame k shows the record whose annotated_frame_index == k",
        },
        "summary": {
            "frames_decoded": stats["frames_decoded"],
            "frames_processed": stats["frames_processed"],
            "frames_without_objects": stats["empty_frames"],
            "observed_detections_by_class": dict(stats["observed_by_class"]),
            "untracked_observed_detections": stats["untracked_detections"],
            "predicted_lost_track_entries": stats["predicted_entries"],
            "unique_track_ids": len(track_ids),
            "track_ids": track_ids,
            "runtime_seconds": round(runtime, 3),
            "inference_ms_median": round(float(np.median(inf)), 2) if inf else None,
            "inference_ms_p90": round(float(np.percentile(inf, 90)), 2) if inf else None,
            "processed_fps_overall": round(stats["frames_processed"] / runtime, 3) if runtime > 0 else None,
        },
        "warnings": warnings,
    }
