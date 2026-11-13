# Codex session 01a05d6f: initial audit, CG-001A and CG-002

Historical record; see [../README.md](../README.md) for authority rules.

## 1. Source

| Field | Value |
| --- | --- |
| Session ID | `01a05d6f-d7c9-7f72-8590-d6af23a35f34` |
| Transcript | `~/.codex/sessions/2026/09/01/rollout-2026-09-01T07-46-45-01a05d6f-….jsonl` (not committed) |
| Thread title | “Audit ContextGuard repository” |
| Turns | Three tasks on two dates: 2026-09-01 14:48Z; 2026-09-27 16:33Z and 16:44–16:50Z. A content-free thread-settings event on 2026-10-07. |
| Client | Codex VS Code extension; CLI `0.151.0-alpha.7.2` at start |
| Model as recorded | `gpt-5.6-sol` (effort low) on 2026-09-01; `gpt-6-astra` (effort medium) on 2026-09-27 |
| Sandbox | Workspace-write, network off, `.git` read-only |

The thread was opened on 2026-09-01 for the first audit and **resumed on 2026-09-27**
for CG-001A and CG-002. Meanwhile, CG-001 itself was run in a separate thread
([01a0e3b4](2026-09-27_01a0e3b4_CG-001-coordination-audit.md)).

---

## Task A: first repository audit (2026-09-01)

### Context

The owner asked Codex to read `MASTER_PLAN.md` completely and do a
**repository audit only**: no modifications, deletions, installs or generated
files. It was to report 16 items: tree, environment, dependencies, source files,
notebooks, CV code, datasets, tests, configs, what runs, what fails, broken
imports, GPU-only assumptions, hard-coded paths, components versus the plan, and
missing components. It was also to classify every module, map the repo to the
plan's development sequence, and propose the **smallest milestone toward the
plan's first vertical slice**:
`recorded video → detection → tracking → zones/object state → structured events →
expected context comparison → anomaly/normal decision → stored JSON/events → evidence window`.

### Findings

- The repo was an **unimplemented shell**: `MASTER_PLAN.md` (68,258 bytes,
  1,763 lines), `.vscode/settings.json` (Conda manager only, *no interpreter
  path*) and empty read-only `.agents/` and `.codex/` folders. `.git` existed
  but was empty: “not a git repository”.
- Shell `python` was Conda **base, Python 3.14.7**, which had no NumPy or OpenCV.
- Conda env **`fyp`, Python 3.10.21**, had OpenCV 5.0.0.93, NumPy 2.2.6,
  ONNX Runtime 1.23.2 (CPU and Azure providers), TensorFlow 2.21.0, Keras
  3.12.4, tflite-runtime 2.14.0, Pillow, PyYAML, matplotlib and Jupyter. Missing:
  PyTorch, torchvision, Ultralytics, any tracker, Supervision, SciPy, pandas,
  Pydantic, FastAPI, SQLAlchemy, pytest, Streamlit, Transformers, Whisper and TTS.
  `pip check` was clean in both environments.
- There was no GPU: `nvidia-smi` was absent, TensorFlow reported “Could not find
  cuda drivers”, and CUDA initialisation failed. The first implementation must
  default to CPU.
- No notebooks, media, datasets, tests, configs, weights or dependency manifest existed.
- Module classification: every module was PLANNED, with audio/NLP, learned temporal
  model, multi-camera, diarisation and live adaptation DEFERRED. The coordinator
  later corrected this (see Task B).

### Proposal (superseded)

The smallest milestone proposed was **one CPU-only, offline, deterministic scenario
that produces a complete event-and-decision artefact**:
- one recorded clip, one person class, one asset class;
- 2–3 polygon zones (entrance, desk, exit), a pretrained detector and a simple tracker;
- states present / moved-carried / outside;
- a versioned event schema, one manual context and one mismatch rule;
- JSON(L) storage and one evidence clip;
- normal and anomaly fixtures with schema, state, context and decision tests.

It also recommended formally recording the Python environment. **Status:**
superseded. CG-002 became inspection only, and the FYP-1 amendment ends the
current executable demo at annotated video plus structured observations.

---

## Task B: CG-001A, closing audit gaps (2026-09-27 16:33Z)

### Context (prompt wording preserved)

“CG-001A — Close audit gaps … resolve these remaining items with read-only checks:”

1. Compare the `MASTER_PLAN.md` SHA-256 with the copy reviewed in the coordinating conversation, `9e161cd5ca5997b6f216e0c22c8e1a5ed68c5a051fc2be777f208b12026af6c1`.
2. Re-read `.vscode/settings.json`. The owner had supplied a version containing `python.defaultInterpreterPath`, but the audit had reported it absent.
3. Report CPU, logical CPUs and RAM visible to WSL; missing `nvidia-smi` alone does not prove there is no GPU.
4. Explicitly invoke the `fyp` interpreter for all later checks.

**Coordination corrections** (verbatim intent):
- Requirements are documented; application modules remain PLANNED.
- Audio and learned temporal modelling remain optional/proposed until scope decisions are recorded.
- Missing object detections must remain distinguishable from observed asset departure.
- Do not install every package in the master plan; select dependencies per milestone.

### Results

- **Hash matched exactly** (`9e161cd5…26af6c1`).
- `.vscode/settings.json` now contained `python.defaultInterpreterPath` →
  `/home/w4shm1337/miniconda3/envs/fyp/bin/python`. When it changed is unverified.
- Hardware: **Intel Core i5-1135G7 @ 2.40 GHz**, 8 logical CPUs (all available),
  **7.63 GiB RAM** (6.11 GiB free), 2 GiB swap, kernel `6.18.33.2-microsoft-standard-WSL2`.
  GPU availability was “undemonstrated”, not disproved.
- Codex accepted the corrected classification: modules PLANNED; audio and learned
  temporal modelling optional/proposed, not yet deferred.

---

## Task C: CG-002, refined scope and recorded-video inspection (2026-09-27 16:44–16:50Z)

### Context (accepted working decisions relayed from the coordinator)

- One university faculty office, initially a staged room. One fixed camera; recorded
  video first; CPU-compatible local development.
- First prototype sessions exclude the office occupant; everyone entering is a visitor.
- Initial assets: one laptop and one backpack at registered starting positions.
- Core anomalies: excess simultaneous visitor occupancy, and asset departure
  inconsistent with explicitly configured session permission.
- Occlusion or lost detection alone must not establish asset departure.
- Audio and accessibility workflows deferred from the current build; this must
  still be communicated to the supervisor.
- Pretrained models first; fine-tune only when observed failures justify it.
- Two students; 2–3 volunteers. Presentation 2026-10-14; year-end working-system target.
- No application functionality existed.

Bounded task: append a dated amendment without claiming supervisor approval;
create concise DECISIONS/PROGRESS/HANDOFF docs; build a **headless inspection
command** using the existing OpenCV with input/output arguments.

The JSON report was to record source metadata, decoded frame count, dimensions,
reported FPS, timing method and warnings. It had to distinguish reported duration
from decoded observations and claim no precise timing. The command should export
a few frames for placement review, handle missing/unreadable/empty input and invalid
metadata, never overwrite footage, and ship with a minimal dependency declaration.
It was to be verified with a temporary synthetic video labelled “strictly as a
software test fixture”.

Explicitly excluded: detection, tracking, dashboard, audio, anomaly logic, the full
stack, Conda base changes and deleting files.

### What was done

All files were written in three patches. Code and tests were written once, with
no later revisions, and the committed versions are identical:

| File | Content |
| --- | --- |
| `MASTER_PLAN.md` | Appended “Scope amendment CG-002 — 2026-09-27”, ending at byte 71,248 with SHA-256 `840f96d4…fb29a2`. The original 68,258 bytes were verified unchanged. |
| `scripts/inspect_video.py` | 185-line CLI: two sequential decode passes (count/dimensions, then first/middle/last JPEG export without seeking); invalid metadata recorded as `null` plus warnings; exclusive-create output; schema `contextguard.video_inspection.v1`; exit codes 0/1/2. |
| `tests/test_inspect_video.py` | 10 `unittest` tests: synthetic MJPEG round trip with source SHA-256 preservation and existing-output refusal; missing, directory, zero-byte and invalid-content input; source-as-output; symlinked output; mocked invalid/non-finite metadata; empty stream; count/dimension mismatch. |
| `requirements.txt` | `opencv-python==5.0.0.93` only (NumPy comes via OpenCV). |
| `README.md` | Minimal setup/run/limitations page. **Replaced** in session [01a0e3d0](2026-09-27_01a0e3d0_github-publication.md); its content moved mainly into `docs/VIDEO_INSPECTION.md`. |
| `docs/DECISIONS.md` | D01–D09 plus CG-002 implementation choices and pending items. |
| `docs/PROGRESS.md` | Component status table. |
| `docs/HANDOFF.md` | Verification commands, outcomes, hashes, limitations and the proposed CG-003. |

Design rationale stated by Codex: timing uses zero-based decoded frame indices,
with clearly labelled index/FPS estimates. Every report carries a warning because
OpenCV read termination cannot distinguish clean EOF from a decode failure. Two
passes avoid trusting container frame counts and avoid seeking.

### Test and command results (2026-09-27)

- `unittest discover`: **10 tests passed in 2.088 s** (fixture dir `/tmp/cg002-software-fixture-a_3uj0ah`).
- `--help` exit 0. Synthetic video: exit 0; 12 frames, 160×120, reported 10 FPS,
  1.2 s metadata duration, samples at 0/5/11 (0/0.5/1.1 s), EOF-ambiguity warning.
- Missing, zero-byte and invalid-content inputs: exit 1 with clear messages and no report.
- `git diff --check` exit 0, but all files were untracked at the time, so it proved little.

### Decisions recorded

D01–D09 in [DECISIONS.md](../../DECISIONS.md), still current.

### Proposals and superseded content

- **Proposed CG-003 = staged pilot capture and placement review**, before selecting a
  perception baseline. *Superseded* by the FYP-1 amendment: pilot and placement
  review became prerequisites inside CG-003 person detection/tracking.
- `docs/HANDOFF.md` statements “No Git commits were created” and “all project files
  are currently untracked” were true on 2026-09-27 and are now historical.

### Open items at the end

Supervisor communication; consented pilot recording; placement review; asset
coordinates; occupancy-limit and permission schema; affirmative-departure
criteria; model selection; later milestone acceptance criteria.

## Status today (2026-11-13)

The CG-002 code, tests and schema are unchanged and still pass (10/10 in 1.63 s).
All Task C open items except “later milestone acceptance criteria” (resolved by the
FYP-1 amendment) remain open.
