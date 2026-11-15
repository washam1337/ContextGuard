"""End-to-end pipeline tests with a scripted fake detector on synthetic video.

Synthetic software fixtures only; these are not ContextGuard research data. The fake
perception exercises the pipeline logic deterministically; real model behaviour must
be validated on consented footage.
"""

import hashlib
import json
import shutil
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

import cv2
import numpy as np

from contextguard.observation import validate_observation
from contextguard.perception import Detection, FramePerception, TrackObservation
from contextguard import pipeline as pipeline_module
from contextguard.pipeline import PipelineConfig, PipelineError, run_pipeline
from contextguard.video import FrameSource

ZONES = {
    "schema_version": "contextguard.zones.v1", "config_id": "fixture-v1", "reference_width": 160,
    "reference_height": 120, "membership_anchors": {"person": "bottom_center"},
    "zones": [{"id": "left", "kind": "entry", "polygon": [[0, 0], [80, 0], [80, 120], [0, 120]]}],
}


class FakePerception:
    """Frame k: person visible on even calls, a lost prediction on odd calls; nothing on call 4."""

    class_names = {0: "person", 63: "laptop"}

    def __init__(self):
        self.calls = 0

    def process(self, frame):
        k = self.calls
        self.calls += 1
        if k == 4:
            return FramePerception([], [], inference_ms=1.0)
        if k % 2 == 0:
            det = Detection(0, "person", 0.9, (10 + k, 20, 40 + k, 110))
            return FramePerception([det], [TrackObservation("person:0001", "tracked", (10 + k, 20, 40 + k, 110),
                                                            0, "person", 0)], inference_ms=1.0)
        return FramePerception([], [TrackObservation("person:0001", "lost", (12 + k, 20, 42 + k, 110),
                                                     0, "person", None)], inference_ms=1.0)

    def describe(self):
        return {"name": "fake-perception-for-tests"}


def make_video(path, n=12, fps=10.0):
    w = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"MJPG"), fps, (160, 120))
    for i in range(n):
        w.write(np.full((120, 160, 3), i * 15, np.uint8))
    w.release()


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="cg-pipeline-fixture-"))
        self.video = self.dir / "synthetic-software-test.avi"
        make_video(self.video)
        self.zones = self.dir / "zones.json"
        self.zones.write_text(json.dumps(ZONES))

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_fake(self, out, **kw):
        cfg = PipelineConfig(input=self.video, output=out, zones=self.zones, **kw)
        return run_pipeline(cfg, perception_factory=lambda c, t: FakePerception())

    def read(self, out):
        return [json.loads(line) for line in (out / "observations.jsonl").read_text().splitlines()]

    def test_outputs_align_and_validate(self):
        before = hashlib.sha256(self.video.read_bytes()).hexdigest()
        out = self.dir / "run"
        m = self.run_fake(out, stride=2)
        recs = self.read(out)
        self.assertEqual(m["status"], "completed")
        self.assertEqual(m["summary"]["frames_decoded"], 12)
        self.assertEqual(len(recs), 6)                                   # every 2nd frame
        self.assertEqual([r["source_frame_index"] for r in recs], [0, 2, 4, 6, 8, 10])
        self.assertEqual([r["annotated_frame_index"] for r in recs], list(range(6)))
        for r in recs:
            validate_observation(r)
            self.assertEqual(r["run_id"], m["run_id"])
        self.assertEqual([r["timestamp"]["estimated_seconds"] for r in recs], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        self.assertEqual(recs[4]["objects"], [])                         # empty frame still recorded
        self.assertEqual(recs[1]["objects"][0]["box_source"], "predicted")
        self.assertEqual(recs[1]["counts"]["visible_persons"], 0)        # predictions not counted
        self.assertEqual(recs[0]["counts"]["per_zone"]["left"]["person"], 1)
        cap = cv2.VideoCapture(str(out / "annotated.mp4"))
        n = 0
        while cap.read()[0]:
            n += 1
        cap.release()
        self.assertEqual(n, len(recs))                                   # one video frame per record
        self.assertEqual(m["outputs"]["annotated_frames"], 6)
        self.assertEqual(m["source"]["sha256"], before)
        self.assertEqual(hashlib.sha256(self.video.read_bytes()).hexdigest(), before)
        self.assertEqual(m["zones"]["config_id"], "fixture-v1")
        self.assertEqual(len(m["zones"]["sha256"]), 64)
        self.assertEqual(m["summary"]["track_ids"], ["person:0001"])
        saved = json.loads((out / "manifest.json").read_text())
        self.assertEqual(saved["run_id"], m["run_id"])

    def test_max_frames_and_no_video(self):
        out = self.dir / "short"
        m = self.run_fake(out, max_frames=3, write_video=False)
        self.assertEqual(len(self.read(out)), 3)
        self.assertIsNone(m["outputs"]["annotated_video"])
        self.assertFalse((out / "annotated.mp4").exists())
        self.assertTrue(all(r["annotated_frame_index"] is None for r in self.read(out)))

    def test_refuses_existing_output_and_bad_inputs(self):
        out = self.dir / "exists"
        out.mkdir()
        with self.assertRaises(PipelineError):
            self.run_fake(out)
        empty = self.dir / "empty.avi"
        empty.touch()
        with self.assertRaises(PipelineError):
            run_pipeline(PipelineConfig(input=empty, output=self.dir / "e"),
                         perception_factory=lambda c, t: FakePerception())
        with self.assertRaises(FileNotFoundError):
            run_pipeline(PipelineConfig(input=self.dir / "missing.mp4", output=self.dir / "m"),
                         perception_factory=lambda c, t: FakePerception())
        with self.assertRaises(PipelineError):
            self.run_fake(self.dir / "s", stride=0)
        with self.assertRaises(PipelineError):
            self.run_fake(self.dir / "c", conf=0.5, count_conf=0.25)

    def test_undecodable_input_fails_with_manifest(self):
        bad = self.dir / "not-a-video.avi"
        bad.write_bytes(b"software test fixture, not a video")
        out = self.dir / "bad"
        with self.assertRaises(Exception):
            run_pipeline(PipelineConfig(input=bad, output=out), perception_factory=lambda c, t: FakePerception())
        m = json.loads((out / "manifest.json").read_text())
        self.assertEqual(m["status"], "failed")
        self.assertIn("Cannot open video", m["error"])


    def test_zones_scale_to_decoded_size_not_reported_size(self):
        """Reported size (320x240) differs from both the decoded frames (160x120) and the
        zone reference (640x480), as with phone rotation metadata. Zones must follow
        the decoded frames: scale 0.25, so the left-half zone spans x 0-80."""
        zones = dict(ZONES, reference_width=640, reference_height=480,
                     zones=[{"id": "left", "kind": "entry",
                             "polygon": [[0, 0], [320, 0], [320, 480], [0, 480]]}])
        self.zones.write_text(json.dumps(zones))

        class MisreportingSource(FrameSource):
            def __init__(self, path):
                super().__init__(path)
                self.metadata = replace(self.metadata, reported_width=320, reported_height=240)

        class RightSidePerson(FakePerception):
            def process(self, frame):                  # anchor x = 120: outside 0-80
                det = Detection(0, "person", 0.9, (100, 20, 140, 110))
                return FramePerception([det], [TrackObservation("person:0001", "tracked",
                                                                det.box, 0, "person", 0)], inference_ms=1.0)

        out = self.dir / "scaled"
        with mock.patch.object(pipeline_module, "FrameSource", MisreportingSource):
            m = run_pipeline(PipelineConfig(input=self.video, output=out, zones=self.zones, max_frames=3),
                             perception_factory=lambda c, t: RightSidePerson())
        self.assertEqual(m["zones"]["applied_scale"], [0.25, 0.25])
        self.assertTrue(all(r["counts"]["per_zone"]["left"]["person"] == 0 for r in self.read(out)))
        self.assertTrue(any("differs from the reported size 320x240" in w for w in m["warnings"]))

if __name__ == "__main__":
    unittest.main()
