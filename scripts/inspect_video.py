"""Headless recorded-video inspection; no detection or anomaly inference."""

import argparse
import json
import math
from pathlib import Path
import sys

import cv2


class InspectionError(Exception):
    """An input or output cannot be inspected safely."""


def positive_metadata(value, name, warnings, integer=False):
    """Unavailable/invalid OpenCV numeric properties become JSON null."""
    if not math.isfinite(value) or value <= 0 or (integer and not value.is_integer()):
        warnings.append(f"Invalid or unavailable reported {name}; recorded as null.")
        return None
    return int(value) if integer else value


def scan_video(capture):
    """Sequentially count decoded frames without trusting container frame counts."""
    warnings = []
    properties = {
        "frame_count": (cv2.CAP_PROP_FRAME_COUNT, True),
        "fps": (cv2.CAP_PROP_FPS, False),
        "width": (cv2.CAP_PROP_FRAME_WIDTH, True),
        "height": (cv2.CAP_PROP_FRAME_HEIGHT, True),
    }
    reported = {
        name: positive_metadata(float(capture.get(prop)), name, warnings, integer)
        for name, (prop, integer) in properties.items()
    }
    count = 0
    dimensions = {}
    stop = "read_returned_false"
    while True:
        try:
            ok, frame = capture.read()
        except cv2.error:
            stop = "decoder_exception"
            warnings.append("OpenCV raised a decoding error; only the decoded prefix is counted.")
            break
        if not ok:
            break
        if frame is None or frame.size == 0:
            stop = "empty_frame"
            warnings.append("Decoder returned an empty frame; decoding stopped.")
            break
        height, width = frame.shape[:2]
        dimensions[(width, height)] = dimensions.get((width, height), 0) + 1
        count += 1
    if count == 0:
        raise InspectionError("No frames decoded: empty video, unsupported codec, or damaged input.")
    warnings.append(
        "OpenCV read termination does not prove clean EOF; an undecodable tail may be undetected."
    )
    if reported["frame_count"] is not None and reported["frame_count"] != count:
        warnings.append("Decoded frame count differs from reported frame count.")
    if len(dimensions) > 1:
        warnings.append("Decoded frame dimensions change within the video.")
    if reported["width"] is not None and reported["height"] is not None:
        if any(size != (reported["width"], reported["height"]) for size in dimensions):
            warnings.append("Decoded dimensions differ from reported dimensions.")
    fps = reported["fps"]
    duration = reported["frame_count"] / fps if fps and reported["frame_count"] else None
    if duration is not None and not math.isfinite(duration):
        duration = None
        warnings.append("Reported duration calculation overflowed; recorded as null.")
    reported["duration_seconds"] = duration
    reported["duration_method"] = "reported_frame_count / reported_fps; not independently measured"
    return {
        "reported": reported,
        "decoded": {
            "frame_count": count,
            "dimensions": [
                {"width": w, "height": h, "frame_count": n}
                for (w, h), n in dimensions.items()
            ],
            "stop_reason": stop,
        },
        "timing": {
            "method": "zero_based_decoded_frame_index; optional index / reported_fps estimate",
            "precise_timestamps_available": False,
            "limitation": "No validated presentation timestamps or wall-clock capture time. "
                          "FPS-based estimates assume constant frame rate and may be wrong for "
                          "variable-rate or damaged video. Decoded count is not measured duration.",
        },
        "warnings": warnings,
    }


def export_frames(source, output, report):
    """Second sequential pass selects first/middle/last decoded indices, without seeking."""
    count = report["decoded"]["frame_count"]
    targets = sorted({0, (count - 1) // 2, count - 1})
    samples = []
    capture = cv2.VideoCapture(str(source))
    try:
        if not capture.isOpened():
            raise InspectionError("Could not reopen input to export review frames.")
        index = 0
        while index <= targets[-1]:
            ok, frame = capture.read()
            if not ok or frame is None or frame.size == 0:
                raise InspectionError("Second decode pass ended early; review frames are incomplete.")
            if index in targets:
                filename = f"frame_{index:08d}.jpg"
                ok, encoded = cv2.imencode(".jpg", frame)
                if not ok:
                    raise InspectionError(f"Failed to encode review frame {index}.")
                with (output / filename).open("xb") as handle:
                    handle.write(encoded.tobytes())
                fps = report["reported"]["fps"]
                estimate = index / fps if fps else None
                if estimate is not None and not math.isfinite(estimate):
                    estimate = None
                samples.append({
                    "path": filename,
                    "decoded_frame_index": index,
                    "estimated_seconds": estimate,
                })
            index += 1
    finally:
        capture.release()
    return samples


def inspect_video(input_path, output_path):
    source = Path(input_path).expanduser().resolve(strict=True)
    if not source.is_file():
        raise InspectionError("Input must be a local regular video file.")
    # Checking readability also produces a clear PermissionError before OpenCV opens it.
    with source.open("rb"):
        pass
    if source.stat().st_size == 0:
        raise InspectionError("Input is empty (zero bytes).")
    output = Path(output_path).expanduser().absolute()
    if output.exists() or output.is_symlink():
        raise InspectionError("Output path already exists; choose a new directory. Nothing overwritten.")
    capture = cv2.VideoCapture(str(source))
    try:
        if not capture.isOpened():
            raise InspectionError("Cannot open video: unreadable content, unsupported codec, or damaged input.")
        backend = capture.getBackendName()
        report = scan_video(capture)
    finally:
        capture.release()
    report.update({
        "schema_version": "contextguard.video_inspection.v1",
        "source": {"path": str(source), "size_bytes": source.stat().st_size},
        "decoder": {"library": "OpenCV", "version": cv2.__version__, "backend": backend},
        "sample_selection": "first, middle, last of decoded prefix; duplicates removed",
    })
    # Exclusive directory creation and file modes protect source/existing artifacts.
    output.mkdir(parents=True, exist_ok=False)
    report["representative_frames"] = export_frames(source, output, report)
    with (output / "inspection.json").open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
        handle.write("\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Local recorded video file")
    parser.add_argument("--output", required=True, type=Path, help="New directory for JSON and JPEGs")
    args = parser.parse_args(argv)
    try:
        report = inspect_video(args.input, args.output)
    except (InspectionError, OSError, cv2.error) as exc:
        print(f"Inspection failed: {exc}", file=sys.stderr)
        print("Any partial output is retained; use a new output directory to retry.", file=sys.stderr)
        return 1
    print(f"Decoded {report['decoded']['frame_count']} frames. Report: {args.output / 'inspection.json'}")
    for warning in report["warnings"]:
        print(f"Warning: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
