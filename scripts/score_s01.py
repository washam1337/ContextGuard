#!/usr/bin/env python3
"""Score S01 pipeline runs against per-second ground truth (docs/S01_RESULTS_PLAN.md).

Implements the frozen plan (D34) exactly:
- matching: label (clip, t) -> observation record with
  source_frame_index == round(t * reported_fps); no window, no smoothing;
- visible-person count, laptop/backpack presence, occluded seconds, person-track
  fragmentation, descriptive zone timelines and speed, per clip and overall, per model;
- primary count_conf 0.25 (from the record's counts), secondary 0.15 / 0.40
  recomputed from the stored observed boxes.

These are development results on the data used for tuning (D30), not a held-out
evaluation, and not a pass of any SYS case. Inputs and outputs live outside the
repository (they come from consented footage).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PRIMARY_CONF = 0.25
SECONDARY_CONFS = (0.15, 0.40)
MIN_TRACK_FRAMES = 15          # plan § 6.5: 0.5 s at 30 fps
VISITORS = {"SC01": 0, "SC02": 1, "SC03": 2, "SC04": 2, "SC05": 1, "SC06": 1, "SC07": 1, "SC08": 1}
OBJECTS = ("laptop", "backpack")
ZONES = ("doorway", "desk_area", "foreground")
LABEL_COLS = ("persons_visible", "laptop_visible", "backpack_visible", "laptop_occluded", "backpack_occluded")


class ScoringError(ValueError):
    """Inputs do not satisfy the plan's assumptions."""


def clip_code(clip_file: str) -> str:
    return clip_file.split("_")[3]


def load_labels(path: Path) -> dict[str, list[dict[str, Any]]]:
    by_clip: dict[str, list[dict[str, Any]]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            row = {"clip_file": r["clip_file"], "t": int(r["time_s"]), "notes": r.get("notes", "") or ""}
            for c in LABEL_COLS:
                v = (r[c] or "").strip()
                if not v.isdigit():
                    raise ScoringError(f"{r['clip_file']} t={r['time_s']}: {c} is {v!r}, not a whole number")
                row[c] = int(v)
            row["unsure"] = "unsure" in row["notes"].lower()
            by_clip[clip_code(r["clip_file"])].append(row)
    return dict(by_clip)


def load_run(run_dir: Path) -> tuple[dict[str, Any], dict[int, dict[str, Any]]]:
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status") != "completed":
        raise ScoringError(f"{run_dir}: run status is {manifest.get('status')!r}")
    records: dict[int, dict[str, Any]] = {}
    with (run_dir / "observations.jsonl").open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            records[rec["source_frame_index"]] = rec
    return manifest, records


def count_observed(rec: dict[str, Any], cls: str, conf: float, zone: str | None = None) -> int:
    n = 0
    for o in rec["objects"]:
        if o["box_source"] != "observed" or o["confidence"] is None or o["class_name"] != cls:
            continue
        if o["confidence"] < conf:
            continue
        if zone is not None and zone not in o["zones"]:
            continue
        n += 1
    return n


def has_predicted(rec: dict[str, Any], cls: str) -> bool:
    return any(o["box_source"] == "predicted" and o["class_name"] == cls for o in rec["objects"])


def person_stats(pairs: list[tuple[int, int]]) -> dict[str, Any]:
    n = len(pairs)
    confusion = {str(t): {"0": 0, "1": 0, "2": 0, "3+": 0} for t in (0, 1, 2)}
    for t, p in pairs:
        confusion.setdefault(str(t), {"0": 0, "1": 0, "2": 0, "3+": 0})[str(p) if p < 3 else "3+"] += 1
    return {
        "seconds": n,
        "exact": sum(t == p for t, p in pairs),
        "exact_rate": round(sum(t == p for t, p in pairs) / n, 4) if n else None,
        "mae": round(sum(abs(t - p) for t, p in pairs) / n, 4) if n else None,
        "over": sum(p > t for t, p in pairs),
        "under": sum(p < t for t, p in pairs),
        "confusion_true_vs_pred": confusion,
    }


def presence_stats(pairs: list[tuple[int, int]]) -> dict[str, Any]:
    tp = sum(t == 1 and p == 1 for t, p in pairs)
    fn = sum(t == 1 and p == 0 for t, p in pairs)
    fp = sum(t == 0 and p == 1 for t, p in pairs)
    tn = sum(t == 0 and p == 0 for t, p in pairs)
    return {
        "seconds": len(pairs), "tp": tp, "fn": fn, "fp": fp, "tn": tn,
        "recall": round(tp / (tp + fn), 4) if tp + fn else None,
        "precision": round(tp / (tp + fp), 4) if tp + fp else None,
    }


def score_clip(rows: list[dict[str, Any]], manifest: dict[str, Any], records: dict[int, dict[str, Any]],
               frame_index: dict[tuple[str, int], int] | None, exclude_unsure: bool = False) -> dict[str, Any]:
    fps = manifest["source"]["reported_fps"]
    use = [r for r in rows if not (exclude_unsure and r["unsure"])]
    matched, missing = [], []
    for r in use:
        fi = round(r["t"] * fps)
        if frame_index is not None:
            expected = frame_index.get((r["clip_file"], r["t"]))
            if expected is not None and expected != fi:
                raise ScoringError(f"{r['clip_file']} t={r['t']}: frame {fi} != labelling still frame {expected}")
        rec = records.get(fi)
        if rec is None:
            missing.append(r["t"])
            continue
        if rec["counts"]["count_conf"] != PRIMARY_CONF:
            raise ScoringError(f"run count_conf {rec['counts']['count_conf']} != plan {PRIMARY_CONF}")
        recount = count_observed(rec, "person", PRIMARY_CONF)
        if recount != rec["counts"]["visible_persons"]:
            raise ScoringError(f"frame {fi}: recount {recount} != stored {rec['counts']['visible_persons']}")
        matched.append((r, rec, fi))

    out: dict[str, Any] = {"labelled_seconds": len(use), "no_prediction_seconds": missing}
    pairs_primary = [(r["persons_visible"], rec["counts"]["visible_persons"]) for r, rec, _ in matched]
    pairs_secondary = {str(c): [(r["persons_visible"], count_observed(rec, "person", c)) for r, rec, _ in matched]
                       for c in SECONDARY_CONFS}
    out["persons"] = person_stats(pairs_primary)
    out["persons_secondary"] = {c: person_stats(v) for c, v in pairs_secondary.items()}
    out["_pairs"] = {"persons": pairs_primary, "persons_secondary": pairs_secondary}
    out["person_errors"] = [
        {"t": r["t"], "true": r["persons_visible"], "pred": rec["counts"]["visible_persons"]}
        for r, rec, _ in matched if r["persons_visible"] != rec["counts"]["visible_persons"]
    ]
    for obj in OBJECTS:
        pairs = [(r[f"{obj}_visible"], int(rec["counts"]["visible_by_class"].get(obj, 0) >= 1)) for r, rec, _ in matched]
        out[obj] = presence_stats(pairs)
        out["_pairs"][obj] = pairs
        out[f"{obj}_errors"] = [
            {"t": r["t"], "true": t, "pred": p}
            for (r, _, _), (t, p) in zip(matched, pairs) if t != p
        ]
        occ = [(r, rec) for r, rec, _ in matched if r[f"{obj}_occluded"] == 1]
        out[f"{obj}_occluded"] = {
            "seconds": len(occ),
            "counted_anyway": sum(rec["counts"]["visible_by_class"].get(obj, 0) >= 1 for _, rec in occ),
            "predicted_box_kept": sum(has_predicted(rec, obj) for _, rec in occ),
        }
    # Zone timelines at the labelled frames (descriptive only).
    out["zone_timeline"] = {
        z: {cls: "".join(str(min(count_observed(rec, cls, PRIMARY_CONF, z), 9)) for _, rec, _ in matched)
            for cls in ("person",) + OBJECTS}
        for z in ZONES
    }
    out["truth_timeline"] = {c: "".join(str(r[c]) for r, _, _ in matched) for c in LABEL_COLS}
    # Track fragmentation over the whole clip (all frames, not only labelled ones).
    frames_per_track: Counter = Counter()
    for rec in records.values():
        for o in rec["objects"]:
            if o["class_name"] == "person" and o["box_source"] == "observed" and o["track_id"]:
                frames_per_track[o["track_id"]] += 1
    out["person_tracks"] = {
        "total_ids": len(frames_per_track),
        "ids_with_min_frames": sum(n >= MIN_TRACK_FRAMES for n in frames_per_track.values()),
        "min_frames": MIN_TRACK_FRAMES,
        "frames_per_id": dict(sorted(frames_per_track.items())),
    }
    s = manifest["summary"]
    out["speed"] = {"processed_fps_overall": s.get("processed_fps_overall"),
                    "inference_ms_median": s.get("inference_ms_median"),
                    "inference_ms_p90": s.get("inference_ms_p90"),
                    "runtime_seconds": s.get("runtime_seconds"),
                    "frames_processed": s.get("frames_processed")}
    out["run"] = {"run_id": manifest["run_id"], "weights_sha256": manifest["perception"]["weights"]["sha256"],
                  "source_sha256": manifest["source"]["sha256"], "zones_sha256": (manifest.get("zones") or {}).get("sha256"),
                  "code_commit": manifest["code"].get("commit"),
                  "uncommitted_changes": manifest["code"].get("uncommitted_changes")}
    return out


def pool(clips: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Overall metrics: pool the seconds of all clips (not an average of clip rates)."""
    ppairs = [pr for c in clips.values() for pr in c["_pairs"]["persons"]]
    presence = {o: [pr for c in clips.values() for pr in c["_pairs"][o]] for o in OBJECTS}
    secondary = {str(conf): person_stats([pr for c in clips.values() for pr in c["_pairs"]["persons_secondary"][str(conf)]])
                 for conf in SECONDARY_CONFS}
    total_runtime = sum(c["speed"]["runtime_seconds"] or 0 for c in clips.values())
    total_frames = sum(c["speed"]["frames_processed"] or 0 for c in clips.values())
    return {
        "persons": person_stats(ppairs),
        "persons_secondary": secondary,
        **{o: presence_stats(presence[o]) for o in OBJECTS},
        **{f"{o}_occluded": {k: sum(c[f"{o}_occluded"][k] for c in clips.values())
                             for k in ("seconds", "counted_anyway", "predicted_box_kept")} for o in OBJECTS},
        "speed": {"frames": total_frames, "runtime_seconds": round(total_runtime, 2),
                  "fps_overall": round(total_frames / total_runtime, 2) if total_runtime else None},
    }


def choose_demo_model(overall: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Plan § 7: highest person exact-match; ties within 2 points -> laptop recall -> speed."""
    best_rate = max(o["persons"]["exact_rate"] for o in overall.values())
    tied = [m for m, o in overall.items() if best_rate - o["persons"]["exact_rate"] <= 0.02]
    tied.sort(key=lambda m: (-(overall[m]["laptop"]["recall"] or 0), -(overall[m]["speed"]["fps_overall"] or 0)))
    return {"model": tied[0], "best_person_exact_rate": best_rate, "tied_within_2_points": tied}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--labels", required=True, type=Path)
    ap.add_argument("--runs", required=True, type=Path, help="Directory with <model>/<clip>/ run folders")
    ap.add_argument("--models", nargs="+", default=["yolo26n", "yolo26s", "yolo11n", "yolo11s"])
    ap.add_argument("--frame-index", type=Path, help="frame_index.json written with the labelling stills")
    ap.add_argument("--output", required=True, type=Path, help="New JSON file for the results")
    args = ap.parse_args(argv)

    labels = load_labels(args.labels)
    frame_index = None
    if args.frame_index:
        frame_index = {(e["clip"], e["time_s"]): e["frame"] for e in json.loads(args.frame_index.read_text())}
    results: dict[str, Any] = {
        "plan": "docs/S01_RESULTS_PLAN.md (D34)",
        "nature": "development results on the tuning data (D30); not a held-out evaluation; no SYS case run",
        "labels_file": str(args.labels), "labelled_seconds": sum(len(v) for v in labels.values()),
        "unsure_rows": sum(r["unsure"] for v in labels.values() for r in v),
        "models": {},
    }
    for model in args.models:
        clips, clips_no_unsure = {}, {}
        for sc in sorted(labels):
            manifest, records = load_run(args.runs / model / sc)
            clips[sc] = score_clip(labels[sc], manifest, records, frame_index)
            clips_no_unsure[sc] = score_clip(labels[sc], manifest, records, frame_index, exclude_unsure=True)
            clips[sc]["visitors_from_log"] = VISITORS.get(sc)
        results["models"][model] = {"overall": pool(clips),
                                    "overall_excluding_unsure": pool(clips_no_unsure),
                                    "clips": clips}
        for c in clips.values():
            c.pop("_pairs")
    results["demo_model_rule"] = choose_demo_model({m: v["overall"] for m, v in results["models"].items()})
    with args.output.open("x", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
