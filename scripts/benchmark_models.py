"""CPU speed/detection benchmark of candidate YOLO weights on one recorded video.

Detection only (no tracking). Models run in a randomised order with warm-up frames
excluded, to reduce run-order bias. Use tuning takes only; this does not measure
accuracy (it has no ground truth). It reports speed and raw detection counts.
"""

import argparse
import json
import random
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import cv2  # noqa: E402

from contextguard.perception import DEFAULT_CLASSES, sha256_file  # noqa: E402


def frames(path, n, stride):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"Cannot open {path}")
    i = got = 0
    try:
        while got < n:
            ok, f = cap.read()
            if not ok:
                break
            if i % stride == 0:
                got += 1
                yield f
            i += 1
    finally:
        cap.release()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--weights", required=True, nargs="+", type=Path)
    p.add_argument("--frames", type=int, default=120)
    p.add_argument("--warmup", type=int, default=5)
    p.add_argument("--stride", type=int, default=1)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--conf", type=float, default=0.25)
    p.add_argument("--threads", type=int, default=4)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--output", type=Path, help="Write JSON results here (must not exist)")
    a = p.parse_args(argv)

    import torch
    from ultralytics import YOLO

    torch.set_num_threads(a.threads)
    order = list(a.weights)
    random.Random(a.seed).shuffle(order)
    results = []
    for w in order:
        model = YOLO(str(w), task="detect")
        times, counts, n = [], {v: 0 for v in DEFAULT_CLASSES.values()}, 0
        for k, f in enumerate(frames(a.input, a.frames + a.warmup, a.stride)):
            s = time.perf_counter()
            r = model.predict(f, imgsz=a.imgsz, conf=a.conf, classes=list(DEFAULT_CLASSES), device="cpu",
                              verbose=False)[0]
            dt = (time.perf_counter() - s) * 1000
            if k < a.warmup:
                continue
            times.append(dt)
            n += 1
            for c in r.boxes.cls.tolist():
                counts[DEFAULT_CLASSES[int(c)]] += 1
        results.append({
            "weights": w.name, "sha256": sha256_file(w), "frames": n,
            "ms_median": round(statistics.median(times), 1) if times else None,
            "ms_p90": round(sorted(times)[int(0.9 * (len(times) - 1))], 1) if times else None,
            "fps": round(1000 / statistics.median(times), 2) if times else None,
            "detections_per_frame": {k: round(v / n, 3) if n else None for k, v in counts.items()},
        })
    report = {"input": str(a.input), "imgsz": a.imgsz, "conf": a.conf, "threads": a.threads,
              "run_order": [w.name for w in order], "results": sorted(results, key=lambda r: r["weights"]),
              "note": "Speed and raw detection rates only; no ground truth, so not accuracy."}
    text = json.dumps(report, indent=2)
    if a.output:
        with a.output.open("x") as fh:
            fh.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
