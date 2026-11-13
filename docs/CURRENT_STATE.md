# Current state and resume guide

**Last updated:** 2026-11-13 by Claude Code (handoff from Codex/ChatGPT).
This is a living document. Update it at the end of every milestone or significant
session. Everything below marked *verified* was checked by running commands on
2026-11-13. Nothing here is a research result.

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
Only the CG-002 recorded-video inspector is implemented.

## 2. Where knowledge lives

| Need | Read |
| --- | --- |
| Agent rules and authority order | [`CLAUDE.md`](../CLAUDE.md) |
| Current scope, deliverables, milestones, SYS cases, observation contract | [`MASTER_PLAN.md` § FYP-1 amendment](../MASTER_PLAN.md#fyp-1-scope-amendment--2026-10-24) |
| Narrowed domain, assets, anomalies, deferrals | [`MASTER_PLAN.md` § CG-002 amendment](../MASTER_PLAN.md#scope-amendment-cg-002--2026-09-27) |
| Research question, ablation, metrics, error analysis, ethics, novelty limits | `MASTER_PLAN.md` §1, §10, §11, §13, §24, §30, §39 (original spec, still valid as research direction) |
| Decision log D01–D19 | [`docs/DECISIONS.md`](DECISIONS.md) |
| Status log | [`docs/PROGRESS.md`](PROGRESS.md) |
| Inspector usage and report schema | [`docs/VIDEO_INSPECTION.md`](VIDEO_INSPECTION.md) |
| CG-002 verification record (historical) | [`docs/HANDOFF.md`](HANDOFF.md) |
| How we got here; superseded proposals; Codex sessions | [`docs/history/`](history/README.md) |

## 3. Verified repository and environment state (2026-11-13)

| Item | State |
| --- | --- |
| Branch | `main`, tracking `origin/main` (public: `github.com/washam1337/ContextGuard`) |
| Commits | 2026-11-13: `f2969af` “docs: complete Claude Code project handoff” (pushed), followed by a README/status update commit (pushed with owner approval). Run `git log --oneline -3` and `git status` to confirm. |
| Git author | Repository-local identity set 2026-11-13 to the owner's GitHub `noreply` address (owner approved). Earlier history was not rewritten. |
| Other refs | `local-preparation` → `e931d52`: orphan, never pushed, tree identical to `dd765fe`. Kept on purpose; **do not delete without owner approval.** |
| CI | GitHub Actions passed on both pushes (runs 36336320051, 40039326735) |
| Tests | `unittest`: **10/10 pass** in 1.63 s with the `fyp` interpreter. Tests must be run from the repo root (they import `scripts.inspect_video`). |
| `MASTER_PLAN.md` integrity | Append-only confirmed. The original 68,258 bytes have SHA-256 `9e161cd5…26af6c1`; the CG-002 version (71,248 bytes, `840f96d4…fb29a2`) is an exact prefix; current full file is `2469ce9f…6525a142` (84,037 bytes). |
| Interpreter | `/home/w4shm1337/miniconda3/envs/fyp/bin/python`, Python 3.10.21 |
| Declared deps | `opencv-python==5.0.0.93` only (NumPy 2.2.6 comes with it) |
| Undeclared but installed in `fyp` | TensorFlow 2.21.0, Keras 3.12.4, tflite-runtime 2.14.0, **ONNX Runtime 1.23.2 (CPU provider)**, Jupyter, matplotlib, Pillow, PyYAML, jsonschema. All predate the project's Codex work; none are used. |
| Not installed | PyTorch, torchvision, Ultralytics, any tracker library, SciPy, pandas, Pydantic, pytest |
| Hardware | Intel i5-1135G7 (4 cores / 8 threads), 7.6 GiB RAM, 2 GiB swap, no GPU exposed to WSL2 |
| OpenCV build | FFmpeg enabled, GStreamer disabled |
| Real footage / dataset / weights | **None exist** in the repo or ignored folders |

## 4. Status by deliverable and milestone

| Item | Status |
| --- | --- |
| CG-001/CG-001A audits | Complete (history only) |
| **CG-002** recorded-video inspection | **IMPLEMENTED**. Synthetic software validation only. Preserve it and schema `contextguard.video_inspection.v1`. |
| **CG-003** person detection/tracking (includes consented pilot and placement review) | **PLANNED. Next milestone. Blocked on owner approval and on a consented pilot recording.** |
| CG-004 counting/zones | PLANNED |
| CG-005 laptop/backpack detection/tracking | PLANNED. Document detection is EXPERIMENTAL (not started). |
| CG-006 integration/testing/evaluation | PLANNED |
| Deliverable 1: complete workflow diagram | PLANNED. Existing diagrams are conceptual and do not satisfy it. |
| Deliverable 4: dataset and model docs | PLANNED. No dataset, model or weights. |
| SYS-01–SYS-08 | Defined; all **PLANNED / NOT RUN** |
| Audio, accessibility | DEFERRED |
| Learned temporal modelling | Optional/proposed |

## 5. Active gates (owner instructions of 2026-11-13, until lifted)

- Do **not** begin CG-003 implementation.
- Do not modify existing schemas.
- Do not install packages or download models.
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
- The completion target is **2026-12-31**. As of 2026-11-13 that is about 7 weeks
  away, and revised FYP-1 dates are still pending.

## 7. Known gaps and inconsistencies (fixes need owner approval)

1. `README.md` was updated for FYP-1 on 2026-11-13 (status box, capabilities,
   roadmap, docs table). Its Mermaid diagram still shows only the original
   inspection → planned pipeline. The complete workflow diagram is FYP-1
   deliverable 1 and remains PLANNED.
2. `CONTRIBUTING.md` points only to the CG-002 amendment.
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
7. Tests fail if run from outside the repo root (import path), and every run leaves a
   `/tmp/cg002-software-fixture-*` folder by design.
8. The inspector records file size but no checksum. The FYP-1 observation contract
   requires a source checksum, which belongs in new code, not a v1 schema change.
9. Untested inspector paths: decoder exception, empty frame, early end of the second
   pass, JPEG encode failure, permission-denied input. Never run on real footage.
10. The `fyp` environment contains large undeclared packages, which could mask
    missing declarations once new dependencies are added.

## 8. Open decisions

**Governance and schedule**
- Revised FYP-1 dates and the university deadline/format for FYP-1 deliverables.
- Supervisor: identity, whether the scope refinement was communicated, and the presentation outcome.
- Second team member and division of work (D08 says two students).
- Repository licence. This affects which model licences are compatible; see below.
- Branch workflow: `CONTRIBUTING.md` asks for feature branches and PRs, but history shows direct commits to `main`.

**Data (blocks CG-003)**
- Consent form and process; who records; storage location (never this public repo);
  retention and access.
- Camera placement, resolution and FPS. Registered starting positions for laptop and backpack.
- Ground-truth annotation method and tool for person tracks.

**CG-003 technical** (to be proposed with evidence, not assumed)
- Detector and tracker. Criteria: CPU throughput on the i5-1135G7, person-class
  quality at office distances, licence compatibility with a public repo, and
  dependency weight. As generally understood, Ultralytics YOLO is AGPL-3.0 and
  ByteTrack's reference implementation is MIT. Re-verify every licence from the
  source at selection time.
- Runtime: PyTorch (not installed) or ONNX Runtime (already installed).
- Input size, confidence thresholds, frame stride.
- Observation schema v1 (`contextguard.observation.v1`, JSONL suggested) and its validation.
- Timing basis: frame index ÷ FPS, or decoder timestamps (`CAP_PROP_POS_MSEC`) with verification.
- Annotated-video codec/container that actually plays (OpenCV writer availability).
- Code layout: keep `scripts/` or introduce a package (e.g. `contextguard/`) so tests do not depend on the working directory.

**CG-004/CG-005/later**
- Zone purposes in FYP-1 (doorway/entry, desk/asset, restricted); membership anchor;
  boundary and overlap rules.
- Counting policy (confirmed tracks only?); whether occupancy inference exists in
  FYP-1 or stays `null`; entry/exit boundary; how duration thresholds start and reset.
- How a tracker ID is linked to a registered asset ID.
- Permission schema; affirmative departure criteria; SYS-case inputs and thresholds;
  numeric evaluation targets.

## 9. Exact next recommended action

1. *(Done 2026-11-13: handoff committed and pushed; README updated.)*
2. **Owner:** answer the open questions that only the owner can answer (§8
   governance/data): revised FYP-1 deadline and format, presentation outcome,
   supervisor communication, consent arrangements, whether any footage exists.
3. **Owner (critical path, human-only):** arrange a short **consented staged pilot
   recording**: fixed camera, visible doorway, laptop and backpack at their starting
   positions, 1–3 visitors entering and leaving. Store it outside the repository.
4. **Claude, after the owner approves starting CG-003:** produce a *CG-003 plan* first,
   with no code. The plan covers:
   - the pilot recording and consent checklist;
   - placement-review steps using `scripts/inspect_video.py`;
   - a detector/tracker shortlist with licence and CPU-runtime criteria and a benchmark method;
   - draft observation schema v1;
   - the evaluation protocol for missed detections, ID switches and runtime;
   - the list of dependencies to install, for owner approval.

   Implementation starts only after the plan is approved.

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
