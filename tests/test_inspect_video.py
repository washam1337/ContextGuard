"""Synthetic software fixtures only; these are not ContextGuard research data."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import cv2
import numpy as np

from scripts.inspect_video import InspectionError, scan_video


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "inspect_video.py"


class FakeCapture:
    def __init__(self, properties, frames):
        self.properties = properties
        self.frames = iter(frames)

    def get(self, prop):
        return self.properties.get(prop, 0.0)

    def read(self):
        return next(self.frames, (False, None))


class InspectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Retained in /tmp for manual review; no pre-existing files are removed.
        cls.fixture_dir = Path(tempfile.mkdtemp(prefix="cg002-software-fixture-"))
        cls.video = cls.fixture_dir / "synthetic-software-test.avi"
        writer = cv2.VideoWriter(str(cls.video), cv2.VideoWriter_fourcc(*"MJPG"), 10.0, (160, 120))
        if not writer.isOpened():
            raise RuntimeError("Existing OpenCV cannot create the MJPEG software fixture.")
        try:
            for index in range(12):
                frame = np.full((120, 160, 3), index * 15, dtype=np.uint8)
                cv2.putText(frame, f"TEST {index}", (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 255), 1)
                writer.write(frame)
        finally:
            writer.release()
        print(f"\nSynthetic software fixture directory (NOT research data): {cls.fixture_dir}")

    def run_cli(self, source, output):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--input", str(source), "--output", str(output)],
            capture_output=True, text=True, check=False,
        )

    def test_synthetic_video_and_source_preservation(self):
        before = hashlib.sha256(self.video.read_bytes()).hexdigest()
        output = self.fixture_dir / "valid-review"
        result = self.run_cli(self.video, output)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((output / "inspection.json").read_text())
        self.assertEqual(report["schema_version"], "contextguard.video_inspection.v1")
        self.assertEqual(report["decoded"]["frame_count"], 12)
        self.assertEqual(report["decoded"]["dimensions"], [
            {"width": 160, "height": 120, "frame_count": 12}
        ])
        self.assertAlmostEqual(report["reported"]["fps"], 10)
        self.assertAlmostEqual(report["reported"]["duration_seconds"], 1.2)
        self.assertFalse(report["timing"]["precise_timestamps_available"])
        self.assertTrue(any("EOF" in warning for warning in report["warnings"]))
        samples = report["representative_frames"]
        self.assertEqual([sample["decoded_frame_index"] for sample in samples], [0, 5, 11])
        self.assertEqual([sample["estimated_seconds"] for sample in samples], [0, 0.5, 1.1])
        for sample in samples:
            frame = cv2.imread(str(output / sample["path"]))
            self.assertEqual(frame.shape[:2], (120, 160))
        self.assertEqual(hashlib.sha256(self.video.read_bytes()).hexdigest(), before)
        report_bytes = (output / "inspection.json").read_bytes()
        retry = self.run_cli(self.video, output)
        self.assertEqual(retry.returncode, 1)
        self.assertIn("already exists", retry.stderr)
        self.assertEqual((output / "inspection.json").read_bytes(), report_bytes)

    def test_missing_input(self):
        output = self.fixture_dir / "missing-review"
        result = self.run_cli(self.fixture_dir / "missing.mp4", output)
        self.assertEqual(result.returncode, 1)
        self.assertIn("No such file", result.stderr)
        self.assertFalse(output.exists())

    def test_directory_input(self):
        result = self.run_cli(self.fixture_dir, self.fixture_dir / "directory-review")
        self.assertEqual(result.returncode, 1)
        self.assertIn("regular video file", result.stderr)

    def test_zero_byte_input(self):
        source = self.fixture_dir / "zero-byte.avi"
        source.touch()
        result = self.run_cli(source, self.fixture_dir / "zero-review")
        self.assertEqual(result.returncode, 1)
        self.assertIn("zero bytes", result.stderr)

    def test_unreadable_content(self):
        source = self.fixture_dir / "invalid-content.avi"
        source.write_bytes(b"This is a software test fixture, not a video.")
        result = self.run_cli(source, self.fixture_dir / "invalid-review")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Cannot open video", result.stderr)

    def test_source_as_output_is_rejected(self):
        before = self.video.read_bytes()
        result = self.run_cli(self.video, self.video)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.video.read_bytes(), before)

    def test_output_symlink_to_source_is_rejected(self):
        alias = self.fixture_dir / "source-alias"
        alias.symlink_to(self.video)
        result = self.run_cli(self.video, alias)
        self.assertEqual(result.returncode, 1)
        self.assertTrue(alias.is_symlink())

    def test_invalid_metadata_preserves_decoded_observations(self):
        frame = np.zeros((8, 10, 3), dtype=np.uint8)
        capture = FakeCapture({
            cv2.CAP_PROP_FPS: float("nan"),
            cv2.CAP_PROP_FRAME_COUNT: float("inf"),
            cv2.CAP_PROP_FRAME_WIDTH: -1,
            cv2.CAP_PROP_FRAME_HEIGHT: 2.5,
        }, [(True, frame)])
        report = scan_video(capture)
        self.assertEqual(report["decoded"]["frame_count"], 1)
        for name in ("fps", "frame_count", "width", "height", "duration_seconds"):
            self.assertIsNone(report["reported"][name])
        json.dumps(report, allow_nan=False)
        self.assertGreaterEqual(len(report["warnings"]), 5)

    def test_opened_but_empty_stream(self):
        with self.assertRaisesRegex(InspectionError, "No frames decoded"):
            scan_video(FakeCapture({}, []))

    def test_count_and_dimension_mismatch(self):
        capture = FakeCapture({
            cv2.CAP_PROP_FRAME_COUNT: 20,
            cv2.CAP_PROP_FPS: 10,
            cv2.CAP_PROP_FRAME_WIDTH: 10,
            cv2.CAP_PROP_FRAME_HEIGHT: 8,
        }, [(True, np.zeros((8, 10, 3), dtype=np.uint8)),
            (True, np.zeros((4, 5, 3), dtype=np.uint8))])
        report = scan_video(capture)
        self.assertEqual(report["reported"]["duration_seconds"], 2)
        self.assertEqual(report["decoded"]["frame_count"], 2)
        warnings = " ".join(report["warnings"])
        self.assertIn("frame count differs", warnings)
        self.assertIn("dimensions change", warnings)
        self.assertIn("dimensions differ", warnings)


if __name__ == "__main__":
    unittest.main()
