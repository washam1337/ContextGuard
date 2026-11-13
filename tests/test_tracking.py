"""Class-wise ByteTrack adapter, using Ultralytics' real tracker with hand-made boxes.

No model weights are needed. Skipped if Ultralytics is not installed.
"""

import importlib.util
import unittest

import numpy as np

HAVE_ULTRALYTICS = importlib.util.find_spec("ultralytics") is not None

TRACKER = {"tracker_type": "bytetrack", "track_high_thresh": 0.25, "track_low_thresh": 0.1,
           "new_track_thresh": 0.25, "track_buffer": 30, "match_thresh": 0.8, "fuse_score": True}


def boxes(rows):
    from ultralytics.engine.results import Boxes
    data = np.array(rows, dtype=np.float32).reshape(-1, 6)  # x1 y1 x2 y2 conf cls
    return Boxes(data, (480, 640))


@unittest.skipUnless(HAVE_ULTRALYTICS, "ultralytics not installed")
class ClassWiseByteTrackTests(unittest.TestCase):
    def setUp(self):
        from contextguard.perception import ClassWiseByteTrack
        self.tracker = ClassWiseByteTrack({0: "person", 63: "laptop"}, TRACKER)

    def step(self, rows):
        return self.tracker.update(boxes(rows), None)

    def test_identity_kept_through_motion_and_short_gap(self):
        ids = []
        for x in (100, 104, 108):
            tracks = self.step([[x, 100, x + 50, 250, 0.9, 0]])
            tracked = [t for t in tracks if t.state == "tracked"]
            self.assertEqual(len(tracked), 1)
            self.assertEqual(tracked[0].detection_index, 0)
            ids.append(tracked[0].track_id)
        self.assertEqual(len(set(ids)), 1)
        self.assertTrue(ids[0].startswith("person:"))

        gap = self.step([])  # detector misses the person for one frame
        self.assertEqual([t.state for t in gap], ["lost"])
        self.assertEqual(gap[0].track_id, ids[0])
        self.assertIsNone(gap[0].detection_index)

        back = [t for t in self.step([[116, 100, 166, 250, 0.9, 0]]) if t.state == "tracked"]
        self.assertEqual(back[0].track_id, ids[0])  # re-found, same anonymous ID

    def test_classes_never_share_a_track(self):
        for _ in range(3):
            tracks = self.step([[100, 100, 200, 300, 0.9, 0], [105, 105, 195, 295, 0.8, 63]])
        tracked = {t.class_name: t for t in tracks if t.state == "tracked"}
        self.assertEqual(set(tracked), {"person", "laptop"})
        self.assertTrue(tracked["laptop"].track_id.startswith("laptop:"))
        # detection_index refers to the full detection list, not the per-class subset
        self.assertEqual(tracked["person"].detection_index, 0)
        self.assertEqual(tracked["laptop"].detection_index, 1)

    def test_low_confidence_detection_does_not_start_a_track(self):
        tracks = self.step([[100, 100, 150, 250, 0.15, 0]])
        self.assertEqual([t for t in tracks if t.state == "tracked"], [])


if __name__ == "__main__":
    unittest.main()
