# ContextGuard — Claude Code instructions

ContextGuard is a FAST NUCES BS-AI final-year research project: context-aware anomaly
detection for one university faculty office. Core contribution: compare **expected**
activity with **observed** activity over time to produce explainable, evidence-backed
*potential-anomaly* alerts for human review. It is not a generic CCTV, object-detection
or theft-detection app.

Claude Code is the project's **sole AI assistant** (since 2026-11-13): architecture,
research, planning, implementation, testing, documentation and self-review. Do not
depend on or wait for ChatGPT/Codex; their history is archived in `docs/history/`.
The student is the project owner and final decision-maker.

## Start of every session

1. Read `docs/CURRENT_STATE.md`. It holds live status, **active gates**, open
   decisions and the exact next action.
2. Check `git status --short --branch` and run the tests (command below).
3. Before any milestone work, read the relevant `MASTER_PLAN.md` amendment and
   `docs/DECISIONS.md`.

## Authority when sources conflict (highest first)

1. Latest explicit owner decisions in conversation, then recorded in `docs/DECISIONS.md`.
2. FYP-1 scope amendment, 2026-10-24 (end of `MASTER_PLAN.md`).
3. CG-002 scope amendment, 2026-09-27 (`MASTER_PLAN.md`).
4. Original specification (top of `MASTER_PLAN.md`): research direction and future
   scope only. Its “Repository AI Operating Contract” development order, first vertical
   slice, MVP table, audio/accessibility requirements and keys/remote examples do
   **not** govern the current build.

Code and test output beat documentation claims; verify, then fix the docs.
`docs/history/` and `docs/HANDOFF.md` are records, never sources of active
requirements. Never claim supervisor approval: none is recorded, and
“user/coordinator approval” means the owner's approval only.

## Documentation map

| File | Role |
| --- | --- |
| `docs/CURRENT_STATE.md` | Live status, gates, gaps, open decisions, next action. Update at the end of each milestone. |
| `MASTER_PLAN.md` | Full spec plus two dated amendments. **Append-only**; never edit existing text. |
| `docs/DECISIONS.md` | Decision log (D01…). Append new D-numbers; never rewrite old ones. |
| `docs/PROGRESS.md` | Dated status log. Append. |
| `docs/PIPELINE.md` | Perception pipeline usage, output schema, count policy, limitations |
| `docs/MODELS.md` | Installed packages, candidate weights (SHA-256), benchmarks, licences |
| `docs/dataset/` | Recording protocol, consent template, labelling template |
| `docs/VIDEO_INSPECTION.md` | CG-002 inspector reference |
| `docs/HANDOFF.md` | Historical CG-002 verification record (do not rewrite) |
| `docs/history/` | Timeline, Codex session summaries, ChatGPT notes, superseded proposals |

## Current phase: FYP-1 (perception foundation + system design)

- Target anomalies (for the later reasoning stage):
  - excess **simultaneous** visitor occupancy beyond the configured allowance, for the
    required duration;
  - observed departure of a registered asset (laptop or backpack) inconsistent with its
    configured removal permission.
- Six FYP-1 deliverables:
  1. complete system workflow diagram;
  2. working CPU recorded-video demo;
  3. structured frame-level detections/tracks;
  4. dataset and pretrained-model documentation;
  5. test cases and honest evaluation, including SYS-01–08 with their real status;
  6. updated architecture, milestones and roadmap.
- Demo: `recorded video → detection → tracking → zones/counting → annotated video + structured output`.
- CG-002 inspection is **IMPLEMENTED**: preserve `scripts/inspect_video.py` and schema
  `contextguard.video_inspection.v1`.
- Milestones: CG-003 people (includes the consented pilot and placement review),
  CG-004 zones/counting and CG-005 laptop/backpack are built as **one combined pipeline**
  (D21). It is PARTIAL: synthetic tests only, real-footage validation pending. Then
  CG-006 integration/evaluation (PLANNED). Exit criteria are in the FYP-1 amendment;
  check `docs/CURRENT_STATE.md` for live status.
- Do not build interaction inference, asset state, events, permission/context
  reasoning, anomaly rules, incidents, evidence clips, dashboard/API or feedback unless
  an approved milestone includes them. They belong in the workflow *diagram*, labelled planned.
- Audio and accessibility: DEFERRED. Document detection: EXPERIMENTAL. Learned temporal
  models: optional, and must beat simpler baselines.
- **Never start a new milestone without explicit owner approval.**

## Domain invariants

- Keep observation, inference, explanation and human feedback separate in code and data.
- Never infer intent. Say “potential anomaly”, “unexpected activity”, “requires review”.
- Anonymous session-scoped track IDs only. No face recognition or identity inference.
  The initial sessions exclude the office occupant, so everyone entering is a visitor.
- Detector class ≠ tracker ID ≠ registered physical asset ID.
- Visible-person count ≠ inferred occupancy ≠ cumulative arrivals. Unavailable occupancy
  is `null`/unknown, never 0 or a copy of the visible count.
- Occlusion, missed detection or track loss is never asset-departure evidence. Removal
  permission is `permitted | prohibited | unknown`; unknown is not authorisation.
- Brief exceedances must stay distinguishable from persistent ones (duration thresholds).
- Observed boxes ≠ tracker-predicted/interpolated positions. Detector confidence is not
  a calibrated probability.
- The frame-observation schema is versioned and separate from the inspection schema and
  the later event/incident schema. Change any schema only by bumping its version.
- Restricted zones are manually configured, versioned polygons. Zone membership alone is
  not a policy violation.

## Environment and commands

- Always use the explicit interpreter `/home/w4shm1337/miniconda3/envs/fyp/bin/python`
  (Python 3.10.21). Never use or modify Conda base.
- Tests, run from the repo root:
  `/home/w4shm1337/miniconda3/envs/fyp/bin/python -B -m unittest discover -s tests -v`
- CPU only (4-core i5 laptop, 7.6 GiB RAM, no GPU). Pretrained models first; never train
  from scratch; fine-tune only against documented failures.
- **Ask before installing packages or downloading weights.** Add dependencies per
  milestone and pin them in `requirements.txt`. Record model/weights provenance, version,
  licence and SHA-256. Check licence compatibility with a public repository.
- The `fyp` env contains undeclared packages (TensorFlow, ONNX Runtime, Jupyter…). Do not
  rely on anything not declared in `requirements.txt`; CI installs only that file.

## Data, privacy and integrity

- **The GitHub repository is PUBLIC.** Never commit recordings, frames showing real
  people, generated reports, weights, credentials, raw AI transcripts, email addresses or
  other personal data. `.gitignore` covers media, weights and outputs; still review
  `git status` and the staged diff before every commit.
- Never modify source recordings; write outputs to new directories.
- Synthetic fixtures are software test data, never research data.
- Never fabricate metrics, results, dataset size, model performance, test passes,
  completed milestones or approvals. SYS-01–SYS-08 stay **PLANNED / NOT RUN** until
  actually executed with defined inputs; a perception demo does not pass them, and a
  missing alert from an unimplemented engine is not a passing negative case.
- Evaluation integrity:
  - Specify footage, ground truth, matching rules, metrics and thresholds before
    judging performance. Numeric targets are agreed in advance, never retrofitted.
  - Keep tuning and evaluation sessions separate (split by session wherever possible).
  - Report every defined scenario, including failures.
  - Keep the research comparison testable: visual-only vs +temporal vs +context vs
    +temporal+context. Improvements are hypotheses, not expected results.
- Status labels: IMPLEMENTED, PARTIAL, PLANNED, DEFERRED, EXPERIMENTAL.

## Workflow

1. Read the relevant docs and inspect the code before changing anything.
2. Propose a concise plan with decisions and risks; wait for approval on anything material.
3. Implement only the approved scope; no broad refactors without justification.
4. Deterministic logic gets deterministic tests; ML behaviour is validated on identified,
   consented footage, with failures reported alongside successes.
5. Run the tests and inspect the outputs; report changed files, actual results,
   limitations and next steps.
6. Update `docs/CURRENT_STATE.md`, append to `docs/PROGRESS.md` and `docs/DECISIONS.md`,
   and (with approval) `README.md` when status changes.
7. Commit and push only when the owner asks. Show proposed `README.md` changes before
   applying them. Wait for owner review before the next milestone.
8. Explain technical choices plainly. The owner is learning the engineering too.
