"""Run the FYP-1 perception pipeline on a recorded video.

recorded video → detection → tracking → zones/counting → annotated video + structured output.
Observation only: no interaction, departure, permission or anomaly inference.
"""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from contextguard.pipeline import DEFAULT_TRACKER_CONFIG, PipelineConfig, PipelineError, run_pipeline  # noqa: E402
from contextguard.video import CODECS, VideoError  # noqa: E402
from contextguard.zones import ZoneConfigError  # noqa: E402


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path, help="Local recorded video file")
    p.add_argument("--output", required=True, type=Path, help="New output directory (must not exist)")
    p.add_argument("--weights", required=True, type=Path, help="YOLO weights file, e.g. weights/yolo26n.pt")
    p.add_argument("--zones", type=Path, help="Zone configuration JSON (contextguard.zones.v1)")
    p.add_argument("--tracker-config", type=Path, default=DEFAULT_TRACKER_CONFIG)
    p.add_argument("--imgsz", type=int, default=640, help="Detector input size (default 640)")
    p.add_argument("--conf", type=float, default=0.10, help="Detector confidence threshold (default 0.10)")
    p.add_argument("--count-conf", type=float, default=0.25, help="Confidence needed to be counted (default 0.25)")
    p.add_argument("--iou", type=float, default=0.7, help="Detector NMS IoU threshold")
    p.add_argument("--stride", type=int, default=1, help="Process every Nth decoded frame")
    p.add_argument("--max-frames", type=int, help="Stop after this many processed frames")
    p.add_argument("--threads", type=int, help="CPU threads for PyTorch")
    p.add_argument("--codec", choices=sorted(CODECS), default="mp4v", help="Annotated video codec")
    p.add_argument("--no-video", action="store_true", help="Skip the annotated video")
    a = p.parse_args(argv)
    cfg = PipelineConfig(input=a.input, output=a.output, weights=a.weights, zones=a.zones,
                         tracker_config=a.tracker_config, imgsz=a.imgsz, conf=a.conf,
                         count_conf=a.count_conf, iou=a.iou, stride=a.stride, max_frames=a.max_frames,
                         write_video=not a.no_video, codec=a.codec, threads=a.threads,
                         argv=["scripts/run_pipeline.py", *argv])
    try:
        m = run_pipeline(cfg)
    except (PipelineError, VideoError, ZoneConfigError, OSError, ValueError) as exc:
        print(f"Pipeline failed: {exc}", file=sys.stderr)
        print("Any partial output is kept for diagnosis; use a new output directory to retry.", file=sys.stderr)
        return 1
    s = m["summary"]
    print(f"Run {m['run_id']}: {s['frames_processed']} frames processed "
          f"({s['processed_fps_overall']} frames/s overall, median inference {s['inference_ms_median']} ms).")
    print(f"Observed detections: {s['observed_detections_by_class']}; unique track IDs: {s['unique_track_ids']}.")
    print(f"Outputs in {a.output}")
    for w in m["warnings"]:
        print(f"Warning: {w}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
