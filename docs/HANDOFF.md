# CG-002 handoff — 2026-09-27

This task records refined scope and implements recorded-video inspection only.
The user/coordinator accepted the scope; supervisor communication is still pending.

## Review the actual changes

- [Scope amendment](../MASTER_PLAN.md#scope-amendment-cg-002--2026-09-27): appended;
  original specification preserved, conflicting current-build requirements superseded.
- [Inspector source](../scripts/inspect_video.py): complete CLI and inspection logic.
- [Verification source](../tests/test_inspect_video.py): synthetic integration tests
  and mocked invalid-metadata/decoder cases, using standard-library unittest.
- [Dependency declaration](../requirements.txt): existing OpenCV only.
- [Setup and usage](../README.md), [decisions](DECISIONS.md), [progress](PROGRESS.md).

## Verification

All commands below were executed from `/home/w4shm1337/fyp`, with the explicit fyp
interpreter. No package installation or model download occurred.

```bash
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B -c 'import sys, cv2; print(sys.executable); print(cv2.__version__)'
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B -m unittest discover -s tests -v
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B scripts/inspect_video.py --help
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B scripts/inspect_video.py --input /tmp/cg002-software-fixture-a_3uj0ah/synthetic-software-test.avi --output /tmp/cg002-software-fixture-a_3uj0ah/manual-review
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B scripts/inspect_video.py --input /tmp/cg002-software-fixture-a_3uj0ah/missing.mp4 --output /tmp/cg002-software-fixture-a_3uj0ah/manual-missing
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B scripts/inspect_video.py --input /tmp/cg002-software-fixture-a_3uj0ah/zero-byte.avi --output /tmp/cg002-software-fixture-a_3uj0ah/manual-empty
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B scripts/inspect_video.py --input /tmp/cg002-software-fixture-a_3uj0ah/invalid-content.avi --output /tmp/cg002-software-fixture-a_3uj0ah/manual-invalid
```

Outcomes in command order:

1. Exit 0: expected interpreter, OpenCV runtime 5.0.0 (distribution 5.0.0.93).
2. Exit 0: 10 tests passed in 2.088 seconds. Tests cover a real synthetic MJPEG
   encode/decode round trip, source SHA-256 preservation, existing-output refusal,
   source/symlink output refusal, missing/directory/zero-byte/unreadable-content
   inputs, mocked zero-decoded-frame stream, invalid/nonfinite metadata, and
   mismatched reported counts/dimensions. Test subprocesses use `sys.executable`,
   which is the explicitly selected fyp interpreter. No pytest dependency.
3. Exit 0: documented CLI arguments shown.
4. Exit 0: 12 decoded frames, 160×120, reported 10 FPS, metadata-derived duration
   1.2 seconds, samples at indices 0/5/11 (estimated 0/0.5/1.1 seconds). JSON and
   three JPEGs written. Expected EOF/decode ambiguity warning emitted.
5. Exit 1: missing file clearly reported; no report produced.
6. Exit 1: zero-byte input clearly reported; no report produced.
7. Exit 1: unsupported/unreadable video content clearly reported; no report produced.

Synthetic artifacts are retained at `/tmp/cg002-software-fixture-a_3uj0ah` for local
review. They may disappear when temporary storage is cleared. The tests recreate
equivalent fixtures in a new temporary directory on each run. They are not research
data. Existing source footage was not modified or deleted.

Traceability verification command (exit 0):

```bash
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B -c 'import hashlib; from pathlib import Path; data = Path("MASTER_PLAN.md").read_bytes(); expected = "9e161cd5ca5997b6f216e0c22c8e1a5ed68c5a051fc2be777f208b12026af6c1"; original = hashlib.sha256(data[:68258]).hexdigest(); assert original == expected; print("Original 68258 bytes preserved:", original); print("Amended SHA-256:", hashlib.sha256(data).hexdigest())'
```

The original 68,258 bytes retain the coordinating copy's SHA-256
`9e161cd5ca5997b6f216e0c22c8e1a5ed68c5a051fc2be777f208b12026af6c1`.
The amended complete file's SHA-256 is
`840f96d49be62cf01fe36e68d056a8b1f5ecfb57b827a1bc99b2b31325fb29a2`.

`git diff --check` exited 0, but all project files are currently untracked, so that
command alone does not validate their contents. Source and generated JSON were
also inspected directly. The .git directory now contains metadata; the earlier
audit's empty-directory observation is historical. No Git commits were created.

## Limitations and next task

No real office footage has been supplied or assessed. Synthetic media is strictly
a software fixture and is not a research dataset or perception benchmark.
OpenCV metadata may be wrong; frame-index/FPS estimates are not validated timestamps.
Read termination cannot distinguish clean EOF from all decode errors. A readable
prefix may produce a report with warnings. Samples cover the decoded prefix only.
Two sequential decode passes cost more time than one; concurrent source changes
are unsupported. Failed exports retain partial outputs for inspection/recovery.
No model, detection, tracking, dashboard, audio, anomaly logic, or evidence-window
functionality is included. Module A remains PARTIAL even though this utility is
IMPLEMENTED. Dependencies were not installed and Conda base was not changed.

Proposed CG-003: obtain a consented short staged pilot with fixed camera, visible
doorway and registered laptop/backpack starting positions; run the inspector and
review placement/occlusion before selecting a CPU pretrained perception baseline.
Communicate the amended scope to the supervisor. No communication was sent by CG-002.

Pilot command (replace input path; choose a new output directory):

```bash
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B scripts/inspect_video.py --input /absolute/path/to/pilot.mp4 --output /tmp/contextguard-pilot-review-001
```
