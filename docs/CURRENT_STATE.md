# Current state and resume guide

**Last updated:** 2026-11-23 by Claude Code (S01 zones approved, D33; results plan approved, D34).
This is a living document. Update it at the end of every milestone or significant
session. The state in §3 was re-checked by running commands on 2026-11-15; the
footage row on 2026-11-21.
Nothing here is a research result.

## 1. One-paragraph orientation

ContextGuard is a FAST NUCES BS-AI final-year research project. It compares
**expected** activity in one university faculty office with **observed** activity
from one fixed camera, over time, to produce explainable, evidence-backed
*potential-anomaly* alerts for human review. Its two target anomalies are:

- excess **simultaneous** visitor occupancy against a configured allowance;
- observed departure of a registered asset (laptop or backpack) that is inconsistent
  with its configured session removal permission (`permitted | prohibited | unknown`).
  An asset is never "departed" merely because it is occluded or lost, and `unknown`
  permission is unresolved, not authorised.

The project is in **FYP-1**: the perception foundation plus the full system design.
The FYP-1 executable demo is
`recorded video → detection → tracking → zones/counting → annotated video + structured output`.
Implemented so far:
- the CG-002 recorded-video inspector (IMPLEMENTED);
- the combined CG-003/004/005 perception pipeline (PARTIAL: tested on synthetic
  fixtures only; the team's office footage, session S01, was recorded on 2026-11-20
  and has passed the technical checks, but the pipeline has not yet been run on it).

## 2. Where knowledge lives

| Need | Read |
| --- | --- |
| Agent rules and authority order | [`CLAUDE.md`](../CLAUDE.md) |
| Current scope, deliverables, milestones, SYS cases, observation contract | [`MASTER_PLAN.md` § FYP-1 amendment](../MASTER_PLAN.md#fyp-1-scope-amendment--2026-10-24) |
| Narrowed domain, assets, anomalies, deferrals | [`MASTER_PLAN.md` § CG-002 amendment](../MASTER_PLAN.md#scope-amendment-cg-002--2026-09-27) |
| Research question, ablation, metrics, error analysis, ethics, novelty limits | `MASTER_PLAN.md` §1, §10, §11, §13, §24, §30, §39 (original spec, still valid as research direction) |
| Decision log D01–D34 | [`docs/DECISIONS.md`](DECISIONS.md) |
| Perception pipeline usage, output schema, count policy | [`docs/PIPELINE.md`](PIPELINE.md) |
| S01 development-results plan (labels, matching rules, metrics) | [`docs/S01_RESULTS_PLAN.md`](S01_RESULTS_PLAN.md) |
| Packages, candidate weights, licences, benchmarks | [`docs/MODELS.md`](MODELS.md) |
| Recording protocol, consent and labelling templates | [`docs/dataset/`](dataset/README.md) |
| Status log | [`docs/PROGRESS.md`](PROGRESS.md) |
| Inspector usage and report schema | [`docs/VIDEO_INSPECTION.md`](VIDEO_INSPECTION.md) |
| CG-002 verification record (historical) | [`docs/HANDOFF.md`](HANDOFF.md) |
| How we got here; superseded proposals; Codex sessions | [`docs/history/`](history/README.md) |

## 3. Verified repository and environment state (2026-11-15)

| Item | State |
| --- | --- |
| Branch | `main`, tracking `origin/main` (public: `github.com/washam1337/ContextGuard`) |
| Commits | Latest: the zone-scaling fix and second review follow-up (2026-11-15), after `881d44a` (review fixes and AGPL-3.0 licence), `d2f2cfa` (D24), `a15c850` (pipeline) and `f2969af` (handoff). Run `git log --oneline -5` and `git status` to confirm the current state. |
| Git author | Repository-local identity set 2026-11-13 to the owner's GitHub `noreply` address (owner approved). Earlier history was not rewritten. |
| Other refs | `local-preparation` → `e931d52`: orphan, never pushed, tree identical to `dd765fe`. Kept on purpose; **do not delete without owner approval.** |
| CI | GitHub Actions passed on every push to `main`. The last verified run is 43729300017 (`881d44a`). Check `gh run list` for later pushes. |
| Tests | `unittest`: **32 run, 32 pass, 0 skipped** (2026-11-15, `fyp` interpreter, repo root): CG-002 ×10 and pipeline ×22. The YOLO smoke test runs only when `weights/yolo26n.pt` exists, and is skipped in CI. **Run from the repo root**: tests import `contextguard` and `scripts`, which are not installed packages. |
| `MASTER_PLAN.md` integrity | Append-only confirmed. The original 68,258 bytes have SHA-256 `9e161cd5…26af6c1`; the CG-002 version (71,248 bytes, `840f96d4…fb29a2`) is an exact prefix; current full file is `2469ce9f…6525a142` (84,037 bytes). |
| Interpreter | `/home/w4shm1337/miniconda3/envs/fyp/bin/python`, Python 3.10.21 |
| Declared deps | `opencv-python==5.0.0.93`; since 2026-11-13 also `torch==2.14.1+cpu`, `torchvision==0.29.2+cpu`, `ultralytics==8.4.212`, `lap==0.5.14` (D23; see [MODELS.md](MODELS.md)). Ultralytics telemetry is disabled. |
| Weights | `weights/` (git-ignored): yolo26n/s and yolo11n/s candidates, SHA-256 recorded in [MODELS.md](MODELS.md). None selected yet. |
| Undeclared but installed in `fyp` | TensorFlow 2.21.0, Keras 3.12.4, tflite-runtime 2.14.0, **ONNX Runtime 1.23.2 (CPU provider)**, Jupyter, matplotlib, Pillow, PyYAML, jsonschema. All predate the project's Codex work; none are used. |
| Not installed | SciPy, pandas, Pydantic, pytest |
| Hardware | Intel i5-1135G7 (4 cores / 8 threads), 7.6 GiB RAM, 2 GiB swap, no GPU exposed to WSL2 |
| OpenCV build | FFmpeg enabled, GStreamer disabled |
| Real footage / dataset | **Session S01, recorded 2026-11-20: 10 clips** in `~/contextguard-data/raw/S01/` (outside the repository; never committed): SC01–SC08 plus exploratory DOC01/DOC02; SC09 not recorded. iPhone 13 Pro, `.MOV` H.264 + AAC audio (unused, D31), 1920×1080, constant 30.0 fps, 15–33 s each. All decode fully; decoded size equals reported size; timestamp drift ≤ 10 ms. Camera steady across SC01–SC08 (≤ 3 px); moved ~220 px before DOC01/DOC02. S01 is the only FYP-1 dataset (D29). Session log: `~/contextguard-data/logs/session_log_S01.txt`; checksums: `~/contextguard-data/review/S01_footage_check/S01_originals.sha256`. Details: `PROGRESS.md` 2026-11-21. |

## 4. Status by deliverable and milestone

| Item | Status |
| --- | --- |
| CG-001/CG-001A audits | Complete (history only) |
| **CG-002** recorded-video inspection | **IMPLEMENTED**. Synthetic software validation only. Preserve it and schema `contextguard.video_inspection.v1`. |
| **CG-003 + CG-004 + CG-005, combined pipeline (D21)** | **PARTIAL (2026-11-13).** Implemented and tested on synthetic fixtures only:<br>• `contextguard/` package and `scripts/run_pipeline.py`, documented in [PIPELINE.md](PIPELINE.md);<br>• YOLO + class-wise ByteTrack;<br>• `contextguard.observation.v1` JSONL;<br>• zones `contextguard.zones.v1` with visible/per-zone counts;<br>• annotated MP4 and run manifest;<br>• `scripts/benchmark_models.py`.<br>32 tests pass. **Not yet validated on office footage**: S01 is recorded and checked (2026-11-21); pipeline runs on it are next. Document detection is EXPERIMENTAL: a read-only check found COCO models cannot reliably detect the document (D32). |
| CG-006 integration/testing/evaluation | PLANNED |
| Deliverable 1: complete workflow diagram | PLANNED. Existing diagrams are conceptual and do not satisfy it. |
| Deliverable 4: dataset and model docs | **PARTIAL.** [MODELS.md](MODELS.md) records packages, licences, four candidate weights with SHA-256 and a synthetic benchmark and the S01 document check; [dataset/](dataset/README.md) has the recording protocol (with an "S01 as recorded" section) and consent and labelling templates. S01 recorded and documented; no selected model and no results on footage yet. |
| SYS-01–SYS-08 | Defined; all **PLANNED / NOT RUN** |
| Audio, accessibility | DEFERRED |
| Learned temporal modelling | Optional/proposed |

## 5. Active gates (owner instructions of 2026-11-13, until lifted)

- The combined CG-003–CG-005 pipeline is approved (D21–D23); nothing beyond it.
- Do not modify existing schemas (new schemas get new version names).
- No further package installs or model downloads beyond D23 without approval.
- Do not delete `local-preparation`.
- Do not rewrite historical documentation (append only).
- Do not commit or push without explicit owner approval. (The handoff commit, the
  README update and their push were approved on 2026-11-13.)
- Do not modify `README.md` without first showing the owner the proposed change and getting approval.

When the owner lifts a gate, record it in `DECISIONS.md` and update this section.

## 6. Recovered context (from Codex prompts; was not in the repo before 2026-11-13)

- **Supervisor feedback** (relayed 2026-09-27): “refine the use case and clearly
  specify the behaviours/anomalies to detect.” CG-002's narrowing responds to this.
  Whether the narrowed scope has been communicated to the supervisor is **unknown**.
- The 2026-10-14 presentation needed “a concrete dataset solution and development
  roadmap”. **Its outcome is unrecorded.**
- The completion target is **2026-12-31**.
- **FYP-1 presentation: 2026-11-24 (D20, owner, 2026-11-13).** It will show the
  initial code and a working CV model detecting on office footage that the team
  records itself. Eleven days remain from 2026-11-13; this is now the governing deadline.

## 7. Known gaps and inconsistencies (fixes need owner approval)

1. `README.md` updated on 2026-11-15 for the built pipeline (status, capabilities,
   run instructions, diagram, tests, licence). Its diagram is a summary; the
   complete workflow diagram is FYP-1 deliverable 1 and remains PLANNED.
2. *(Fixed 2026-11-15)* `CONTRIBUTING.md` now points to `CURRENT_STATE.md`, the
   FYP-1 amendment and the AGPL licence.
3. The original “Repository AI Operating Contract” at the top of `MASTER_PLAN.md`
   (development order, first vertical slice, accessibility first-class) is
   overridden for the current phase by amendments 1,800 lines later. `CLAUDE.md`
   now warns about this; the plan text itself is preserved unchanged.
4. `MASTER_PLAN.md` §10.1 lists baselines A, B, C, D but omits *visual + context*,
   which §10.3's ablation includes. Treat the four-way ablation as the plan:
   visual-only, +temporal, +context, +temporal+context; validated feedback is a later extension.
5. The headings of `DECISIONS.md` and `PROGRESS.md` say 2026-09-27, but both now
   contain later sections.
6. `docs/HANDOFF.md` is the historical CG-002 record. Its CG-003 proposal and
   “no commits” statements are superseded, and its “amended SHA” is the 2026-09-27 hash.
7. Tests still fail if run from outside the repo root. Re-checked 2026-11-15: from
   `/tmp`, 8 test modules fail to import (`contextguard` ×7, `scripts` ×1), because
   neither is an installed package. The documented command (run from the repo root)
   works. Every run also leaves a `/tmp/cg002-software-fixture-*` folder (CG-002
   design); the pipeline tests clean up after themselves.
8. The inspector records file size but no checksum. The FYP-1 observation contract
   requires a source checksum, which belongs in new code, not a v1 schema change.
9. Untested inspector paths: decoder exception, empty frame, early end of the second
   pass, JPEG encode failure, permission-denied input. First run on real footage
   2026-11-21: all 10 S01 clips inspected without errors.
10. The `fyp` environment contains large undeclared packages, which could mask
    missing declarations once new dependencies are added.
11. *(Fixed 2026-11-15, owner approved; regression test added.)* Zone scaling bug (found by review, confirmed by code reading):
    `run_pipeline` scales zones to the video's *reported* size. If the decoded frames
    differ from that size (e.g. phone rotation metadata) and the reported size also
    differs from the zone reference size, zones are never re-scaled to the real
    frames. Now zones are scaled from the reference size to the decoded frame size,
    with warnings on a reported/decoded mismatch or a mid-video size change.
12. **Audio in the originals.** Every S01 `.MOV` has an AAC audio track, although the
    consent form says no audio is used. Handling: never used or played; outputs are
    silent; originals unmodified (D31).
13. *(Handled 2026-11-23, D33.)* **Membership anchor vs framing.** The camera is at
    chest height, so people near the desk are cut off at the legs. `S01-office-v1`
    handles this without a schema change: a `foreground` strip along the frame bottom
    catches cut-off people, `desk_area` catches people standing behind the desk, and
    `doorway` uses the feet.
14. *(Fixed 2026-11-21.)* The S01 originals are read-only (`chmod a-w`, run by the
    owner because Claude Code's permission system blocked it) and the Windows
    `Zone.Identifier` file is deleted. Checksums re-verified unchanged afterwards.
15. **Protocol deviations in S01** (listed in `PROGRESS.md` 2026-11-21 and the protocol's
    "S01 as recorded" section): SC04 shows no brief exceedance (~14 s); SC08's laptop is
    put on the PC tower and not returned within the clip; SC02–SC04 do not end empty;
    clips are shorter than the protocol's 30–90 s.

## 8. Open decisions

**Governance and schedule**
- Revised FYP-1 dates and the university deadline/format for FYP-1 deliverables.
- Supervisor: identity, whether the scope refinement was communicated, and the presentation outcome.
- Second team member and division of work (D08 says two students).
- *Resolved:* repository licence is AGPL-3.0 (D25).
- *Resolved:* the name and roll number in `MASTER_PLAN.md` stay as they are (D28).
- Branch workflow: `CONTRIBUTING.md` asks for feature branches and PRs, but history shows direct commits to `main`.

**Data**
- *Resolved:* consent is obtained from all volunteers V1–V3 (D24); footage is in
  `~/contextguard-data/raw/S01/`; SC09 not recorded (no restricted zone in this office).
- *Resolved 2026-11-21:* S01 is the only FYP-1 dataset, no S02 before 2026-11-24 (D29,
  supersedes D27 for FYP-1); development results only (D30); audio never used (D31);
  documents stay EXPERIMENTAL (D32). Camera placement, resolution and FPS are fixed
  by the recording (§3); laptop and backpack starting positions are in the session log.
- Open:
  - retention and deletion date (the consent template leaves it blank);
  - whether a later session (S02) is recorded for FYP-2 (D29 lists the reasons).

**Perception pipeline: settled on 2026-11-13** (D21–D23, see [PIPELINE.md](PIPELINE.md))
- Ultralytics YOLO with PyTorch CPU and class-wise ByteTrack (ONNX route not taken).
- Observation schema `contextguard.observation.v1` (JSONL) with a validator.
- Timing: `source_frame_index / reported_fps`, with the decoder's `pos_msec` recorded but unvalidated.
  On the S01 clips the two differ by at most 10 ms (2026-11-21).
- Annotated video: `mp4v` MP4 (no H.264 without FFmpeg).
- Code layout: `contextguard/` package plus `scripts/` command-line tools.

**Perception pipeline: still open**
- Which of the four weights; input size; detector and count thresholds; stride.
  Chosen on S01 (D30).
- Ground-truth labelling for person tracks (per-second count sheet drafted; ID-switch
  labelling not yet defined).
- Development-results plan (labels, matching rules, metrics), written before any
  results are computed (D30).
- Whether to make `contextguard` installable so tests run from any directory (low priority).

**CG-004/CG-005/later**
- Zone purposes in FYP-1 (doorway/entry, desk/asset, restricted); membership anchor;
  boundary and overlap rules.
- Counting policy (confirmed tracks only?); whether occupancy inference exists in
  FYP-1 or stays `null`; entry/exit boundary; how duration thresholds start and reset.
- How a tracker ID is linked to a registered asset ID.
- Permission schema; affirmative departure criteria; SYS-case inputs and thresholds;
  numeric evaluation targets.

## 9. Exact next recommended action

Deadline: **2026-11-24** presentation (D20). Licence: AGPL-3.0 (D25). The 2026-11-13
schedule slipped: S01 was recorded on 2026-11-20 and is the only dataset (D29).

1. *(Done: handoff, pipeline on synthetic fixtures, S01 recorded 2026-11-20 and
   checked 2026-11-21.)*
2. *(Done 2026-11-21: originals read-only, leftover file deleted; gap 14.)*
3. *(Done 2026-11-23: zones `S01-office-v1` approved, D33.)*
4. *(Done 2026-11-23: [S01_RESULTS_PLAN.md](S01_RESULTS_PLAN.md) approved and frozen, D34.)*
5. **Owner:** label SC01–SC08 in the pre-filled sheet
   `~/contextguard-data/labels/S01_labels.csv` (202 rows), using the per-second stills
   in `~/contextguard-data/labelling/S01/`, **before watching any annotated output**.
6. **Claude:** *(runs started 2026-11-23)* all four models on SC01–SC08 with the
   plan's fixed settings, without video, outputs in `~/contextguard-data/runs/S01/`.
   Nothing is compared with labels until steps 4–5 are done.
7. **Claude:** compute the development results exactly as in the plan; choose the
   demo model by the plan's rule; make annotated demo videos; report every scenario,
   including failures.
8. **Nov 23:** workflow diagram (deliverable 1), SYS-01–08 status table (all PLANNED /
   NOT RUN), doc and README updates (README shown first), demo clips, rehearsal.
9. **Due on Nov 24 (owner, 2026-11-21):** a presentation plus code preparation showing
   the FYP about **30–40% working**, i.e. the perception demo on S01 (D20). Remaining
   owner input: the slide/report format, if the university prescribes one.

**Resume point (2026-11-21):** continue with step 3 (zones) in the next session.

## 10. How to resume in a fresh Claude Code session

```bash
cd /home/w4shm1337/fyp
claude
```

Then ask, for example: “Read CLAUDE.md and docs/CURRENT_STATE.md, verify the
repository state, and tell me the next action.” A fresh session should first run:

```bash
git status --short --branch && git log --oneline -5
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B -m unittest discover -s tests -v
```
