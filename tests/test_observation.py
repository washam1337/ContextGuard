"""Observation record construction, counting policy and schema validation."""

import copy
import unittest

from contextguard.observation import (build_frame_record, build_objects, compute_counts,
                                      validate_observation, ObservationSchemaError)
from contextguard.perception import Detection, FramePerception, TrackObservation, format_track_id
from contextguard.zones import parse_zone_config

ZONES = parse_zone_config({
    "schema_version": "contextguard.zones.v1", "config_id": "t", "reference_width": 100,
    "reference_height": 100, "membership_anchors": {"person": "bottom_center"},
    "zones": [{"id": "left", "polygon": [[0, 0], [50, 0], [50, 100], [0, 100]]}],
})
CLASSES = ["person", "laptop", "backpack"]


def perception():
    dets = [
        Detection(0, "person", 0.90, (10, 10, 30, 80)),    # matched to track person:0001
        Detection(0, "person", 0.15, (60, 10, 80, 80)),    # low confidence, untracked
        Detection(63, "laptop", 0.70, (20, 60, 40, 70)),   # matched to laptop:0001
    ]
    tracks = [
        TrackObservation("person:0001", "tracked", (11, 11, 31, 81), 0, "person", 0),
        TrackObservation("laptop:0001", "tracked", (20, 60, 40, 70), 63, "laptop", 2),
        TrackObservation("person:0002", "lost", (70, 20, 90, 90), 0, "person", None),
    ]
    return FramePerception(dets, tracks)


def record(objects=None, counts=None):
    objects = build_objects(perception(), ZONES) if objects is None else objects
    counts = compute_counts(objects, CLASSES, ZONES.zone_ids, 0.25) if counts is None else counts
    return build_frame_record(run_id="r1", source_frame_index=4, processed_index=2, annotated_frame_index=2,
                              width=100, height=100, estimated_seconds=0.1333333, decoder_pos_msec=None,
                              objects=objects, counts=counts)


class ObservationTests(unittest.TestCase):
    def test_observed_and_predicted_are_kept_apart(self):
        objs = build_objects(perception(), ZONES)
        self.assertEqual([o["track_state"] for o in objs], ["tracked", "untracked", "tracked", "lost"])
        tracked = objs[0]
        self.assertEqual(tracked["bbox_observed"], [10, 10, 30, 80])
        self.assertEqual(tracked["bbox_track"], [11, 11, 31, 81])
        self.assertEqual(tracked["track_id"], "person:0001")
        self.assertEqual(objs[1]["track_id"], None)
        lost = objs[3]
        self.assertEqual((lost["box_source"], lost["bbox_observed"], lost["confidence"]), ("predicted", None, None))
        self.assertEqual(lost["bbox_track"], [70, 20, 90, 90])

    def test_count_policy(self):
        objs = build_objects(perception(), ZONES)
        c = compute_counts(objs, CLASSES, ZONES.zone_ids, count_conf=0.25)
        # Low-confidence person and the predicted (lost) person are not counted.
        self.assertEqual(c["visible_persons"], 1)
        self.assertEqual(c["visible_by_class"], {"person": 1, "laptop": 1, "backpack": 0})
        self.assertEqual(c["per_zone"]["left"], {"person": 1, "laptop": 1, "backpack": 0})
        c_low = compute_counts(objs, CLASSES, ZONES.zone_ids, count_conf=0.10)
        self.assertEqual(c_low["visible_persons"], 2)

    def test_empty_frame_record_is_valid_and_occupancy_is_null(self):
        objs = build_objects(FramePerception([], []), ZONES)
        rec = record(objs)
        validate_observation(rec)
        self.assertEqual(rec["objects"], [])
        self.assertEqual(rec["counts"]["visible_persons"], 0)
        self.assertIsNone(rec["inferred_occupancy"]["value"])
        self.assertFalse(rec["inferred_occupancy"]["available"])
        self.assertFalse(rec["timestamp"]["validated"])

    def test_validator_rejects_contract_violations(self):
        good = record()
        validate_observation(good)

        def broken(mutate):
            r = copy.deepcopy(good)
            mutate(r)
            return r

        cases = [
            lambda r: r.pop("counts"),
            lambda r: r.update(schema_version="contextguard.video_inspection.v1"),
            lambda r: r["inferred_occupancy"].update(value=1),                # occupancy must not be faked
            lambda r: r["objects"][3].update(bbox_observed=[1, 1, 2, 2]),      # prediction with observed box
            lambda r: r["objects"][0].update(track_state="lost"),             # observed box cannot be lost
            lambda r: r["objects"][1].update(track_id="person:0009"),          # untracked with an ID
            lambda r: r["objects"][0].update(confidence=1.5),
            lambda r: r["objects"][0].update(bbox_observed=[30, 10, 10, 80]),  # x2 < x1
            lambda r: r["timestamp"].update(validated=True),
        ]
        for mutate in cases:
            with self.assertRaises(ObservationSchemaError):
                validate_observation(broken(mutate))

    def test_track_id_format(self):
        self.assertEqual(format_track_id("person", 3), "person:0003")


if __name__ == "__main__":
    unittest.main()
