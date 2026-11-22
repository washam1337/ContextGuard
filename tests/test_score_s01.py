"""Deterministic tests for scripts/score_s01.py on hand-made fixtures.

Synthetic software fixtures only (a fake manifest and fake observation records);
not research data.
"""

import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import score_s01 as S

CLIP = "cg_20261120_S01_SC02_t1.MOV"


def obj(cls, conf, zones=(), source="observed", track=None):
    return {"class_name": cls, "confidence": conf if source == "observed" else None, "box_source": source,
            "track_id": track, "zones": list(zones)}


def record(frame, objects, count_conf=0.25):
    counted = [o for o in objects if o["box_source"] == "observed" and o["confidence"] >= count_conf]
    by_class = {c: sum(o["class_name"] == c for o in counted) for c in ("person", "laptop", "backpack")}
    return {"source_frame_index": frame, "objects": objects,
            "counts": {"count_conf": count_conf, "visible_persons": by_class["person"], "visible_by_class": by_class}}


class ScoreTests(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="cg-score-fixture-"))
        # fps 2.0 -> label t maps to frame round(2t): t0->0, t1->2, t2->4
        frames = {
            0: [obj("laptop", 0.9, ["desk_area"])],                                   # truth: 0 persons, laptop visible
            1: [obj("person", 0.9, ["doorway"], track="person:0001")],
            2: [obj("person", 0.9, ["doorway"], track="person:0001"),
                obj("person", 0.2, [], track=None),                                   # below 0.25: not counted
                obj("laptop", 0.1, ["desk_area"])],                                   # below 0.25: not counted
            3: [obj("person", 0.9, ["foreground"], track="person:0001")],
            4: [obj("person", 0.9, ["foreground"], track="person:0001"),
                obj("person", 0.5, ["foreground"], track="person:0002"),
                obj("laptop", None, ["desk_area"], source="predicted", track="laptop:0001")],
        }
        run = self.dir / "runs" / "m1" / "SC02"
        run.mkdir(parents=True)
        (run / "observations.jsonl").write_text("\n".join(json.dumps(record(i, o)) for i, o in frames.items()))
        (run / "manifest.json").write_text(json.dumps({
            "status": "completed", "run_id": "r1", "source": {"reported_fps": 2.0, "sha256": "s"},
            "perception": {"weights": {"sha256": "w"}}, "zones": {"sha256": "z"},
            "code": {"commit": "c", "uncommitted_changes": False},
            "summary": {"processed_fps_overall": 10.0, "runtime_seconds": 0.5, "frames_processed": 5}}))
        self.labels = self.dir / "labels.csv"
        with self.labels.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["clip_file", "time_s", "persons_visible", "laptop_visible", "backpack_visible",
                        "laptop_occluded", "backpack_occluded", "notes"])
            w.writerow([CLIP, 0, 0, 1, 0, 0, 0, ""])
            w.writerow([CLIP, 1, 2, 1, 0, 0, 0, "unsure"])
            w.writerow([CLIP, 2, 2, 0, 0, 1, 0, ""])

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def score(self, **kw):
        labels = S.load_labels(self.labels)
        manifest, records = S.load_run(self.dir / "runs" / "m1" / "SC02")
        return S.score_clip(labels["SC02"], manifest, records, None, **kw)

    def test_matching_and_person_metrics(self):
        r = self.score()
        p = r["persons"]
        # truth 0,2,2 vs predicted 0,1,2 (frame 2 has one counted person; frame 4 two)
        self.assertEqual((p["seconds"], p["exact"], p["over"], p["under"]), (3, 2, 0, 1))
        self.assertAlmostEqual(p["mae"], round(1 / 3, 4))
        self.assertEqual(r["person_errors"], [{"t": 1, "true": 2, "pred": 1}])
        self.assertEqual(r["persons_secondary"]["0.15"]["exact"], 3)    # 0.2 box counts at 0.15
        self.assertEqual(r["no_prediction_seconds"], [])

    def test_presence_occlusion_tracks_and_zones(self):
        r = self.score()
        # laptop truth 1,1,0 vs counted 1,0,0 (0.1 box not counted; predicted box never counted)
        self.assertEqual({k: r["laptop"][k] for k in ("tp", "fn", "fp", "tn")}, {"tp": 1, "fn": 1, "fp": 0, "tn": 1})
        self.assertEqual(r["laptop"]["recall"], 0.5)
        self.assertEqual(r["laptop_occluded"], {"seconds": 1, "counted_anyway": 0, "predicted_box_kept": 1})
        self.assertIsNone(r["backpack"]["recall"])                    # no visible backpack seconds
        self.assertEqual(r["person_tracks"]["total_ids"], 2)
        self.assertEqual(r["person_tracks"]["ids_with_min_frames"], 0)  # far fewer than 15 frames each
        self.assertEqual(r["zone_timeline"]["doorway"]["person"], "010")
        self.assertEqual(r["zone_timeline"]["foreground"]["person"], "002")

    def test_unsure_exclusion_and_missing_frames(self):
        self.assertEqual(self.score(exclude_unsure=True)["persons"]["seconds"], 2)
        with self.labels.open("a", newline="") as f:
            csv.writer(f).writerow([CLIP, 5, 0, 0, 0, 0, 0, ""])          # frame 10 does not exist
        self.assertEqual(self.score()["no_prediction_seconds"], [5])

    def test_frame_index_mismatch_and_bad_label_are_errors(self):
        labels = S.load_labels(self.labels)
        manifest, records = S.load_run(self.dir / "runs" / "m1" / "SC02")
        with self.assertRaises(S.ScoringError):
            S.score_clip(labels["SC02"], manifest, records, {(CLIP, 1): 3})
        self.labels.write_text(self.labels.read_text().replace(f"{CLIP},0,0,1", f"{CLIP},0,x,1"))
        with self.assertRaises(S.ScoringError):
            S.load_labels(self.labels)

    def test_pooling_and_demo_rule(self):
        r = self.score()
        r["_pairs"]  # present before main() strips it
        overall = S.pool({"SC02": r})
        self.assertEqual(overall["persons"]["exact"], 2)
        self.assertEqual(overall["speed"]["fps_overall"], 10.0)
        o = lambda rate, rec, fps: {"persons": {"exact_rate": rate}, "laptop": {"recall": rec}, "speed": {"fps_overall": fps}}
        pick = S.choose_demo_model({"a": o(0.80, 0.5, 20), "b": o(0.79, 0.9, 5), "c": o(0.70, 1.0, 30)})
        self.assertEqual(pick["model"], "b")                          # within 2 points of a; higher laptop recall
        self.assertEqual(sorted(pick["tied_within_2_points"]), ["a", "b"])
        pick = S.choose_demo_model({"a": o(0.80, 0.9, 20), "b": o(0.79, 0.9, 5)})
        self.assertEqual(pick["model"], "a")                          # same recall -> faster


if __name__ == "__main__":
    unittest.main()
