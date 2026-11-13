"""Smoke test of the real detector + tracker on Ultralytics' bundled sample image.

Skipped when weights/yolo26n.pt is absent (e.g. in CI, where weights are not
downloaded). This checks that the model loads and runs. It says nothing about
accuracy on office footage.
"""

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = ROOT / "weights" / "yolo26n.pt"
READY = WEIGHTS.is_file() and importlib.util.find_spec("ultralytics") is not None


@unittest.skipUnless(READY, "weights/yolo26n.pt or ultralytics not available")
class YoloSmokeTests(unittest.TestCase):
    def test_model_loads_detects_and_tracks(self):
        import cv2
        from ultralytics.utils import ASSETS

        from contextguard.perception import YoloByteTrackPerception

        tracker_cfg = json.loads((ROOT / "configs" / "tracker" / "bytetrack.json").read_text())
        p = YoloByteTrackPerception(weights=WEIGHTS, tracker_config=tracker_cfg)
        img = cv2.imread(str(ASSETS / "bus.jpg"))
        for _ in range(3):                      # same image 3 times: tracks should persist
            result = p.process(img)
        self.assertGreaterEqual(sum(d.class_name == "person" for d in result.detections), 1)
        self.assertTrue({d.class_name for d in result.detections} <= {"person", "laptop", "backpack"})
        tracked = [t for t in result.tracks if t.state == "tracked"]
        self.assertGreaterEqual(len(tracked), 1)
        self.assertTrue(all(t.detection_index is not None for t in tracked))
        self.assertEqual(p.describe()["weights"]["sha256"],
                         "9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef")


if __name__ == "__main__":
    unittest.main()
