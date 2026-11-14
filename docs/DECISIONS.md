# Working decisions — 2026-09-27

CG-002 records user/coordinator decisions. Supervisor communication is pending;
supervisor approval is not claimed. The historical CG-002 amendment is in
[MASTER_PLAN.md](../MASTER_PLAN.md#scope-amendment-cg-002--2026-09-27); original scope
is preserved there for traceability.

| ID | Accepted working decision |
| --- | --- |
| D01 | One university faculty office, initially a staged room; one fixed camera; recorded video first; CPU-compatible local work. |
| D02 | Office occupant absent from initial sessions; all entering people are visitors; count simultaneous occupancy, not cumulative arrivals. |
| D03 | One laptop and one backpack at registered starting positions. |
| D04 | Core anomalies: excess simultaneous occupancy; asset departure inconsistent with explicitly configured session permission. |
| D05 | Missing detections, occlusion, and track loss remain distinct from affirmative departure evidence. |
| D06 | Audio and accessibility workflows deferred from current build; tell supervisor about refinement. |
| D07 | Pretrained models first; fine-tune only against observed failures. Learned temporal modelling remains optional/proposed. |
| D08 | Two students; 2–3 volunteers available. Presentation 2026-10-14; working-system target year-end 2026. |
| D09 | Select dependencies per milestone. Explicitly invoke the fyp Python interpreter; do not change Conda base. |

CG-002 implementation choices: OpenCV plus standard library; a new output directory
per inspection; first/middle/last decoded-frame samples; frame-index timing with
labelled FPS estimates; invalid metadata becomes null plus warnings. Two sequential
passes avoid trusting metadata counts or seeking for sample selection.

Pending: supervisor scope discussion, consent and pilot recording, placement review,
registered asset coordinates, occupancy limit/session permission schema, affirmative
departure criteria, model selection, and later milestone acceptance criteria.

## Approved FYP-1 scope — 2026-10-24

The user/coordinator approved the [FYP-1 amendment](../MASTER_PLAN.md#fyp-1-scope-amendment--2026-10-24).
It supersedes conflicting current-phase implementation order, demo acceptance
criteria and milestone definitions; the original specification and completed
CG-002 are preserved. Expected-versus-observed reasoning remains the overall
research objective. This is not supervisor approval.

| ID | Accepted working decision |
| --- | --- |
| D10 | FYP-1 delivers a complete system workflow diagram, working recorded-office-video perception demo, structured detections/tracks, dataset/model documentation, honest tests/evaluation including SYS-01–SYS-08, and updated architecture/milestones/roadmap. |
| D11 | Executable demo: recorded video → detection → tracking → zones/counting → annotated video + structured output. Reasoning, incidents, evidence clips and feedback appear in the system design but remain later planned implementation. |
| D12 | CG-003 person detection/tracking (including pilot/placement prerequisites); CG-004 counting/zones; CG-005 office-object detection/tracking; CG-006 integration/testing/evaluation. Exit criteria are in the amendment; all remain PLANNED. |
| D13 | Keep laptop/backpack as initial assets. Document detection is EXPERIMENTAL and feasibility-dependent, not required for acceptance. Restricted zones are manually configured polygons. |
| D14 | Version frame observations with timestamps/timing basis, anonymous IDs, class/confidence, boxes, zones/counts and reproducible model/run configuration. Keep visible-person count separate from inferred office occupancy; unavailable inference is unknown, not zero. |
| D15 | SYS-01–SYS-08 use the approved definitions in the amendment and are PLANNED / NOT RUN system-level cases. They are separate from CG-002 inspection tests; absent downstream functionality cannot produce a valid pass. |
| D16 | Preserve unknown permission and unknown/unobserved asset states; occlusion/track loss is not confirmed departure. Store feedback separately from predictions. |

The earlier pending milestone-definition item is resolved by this amendment.
Remaining decisions include model/tracker selection, observation/configuration
schemas, polygon/count/occupancy policies, duration threshold semantics, timing
validation, affirmative departure criteria and numerical evaluation targets.
Consent, pilot collection, registered asset positions and supervisor communication
remain pending. The October 14 presentation date is historical with no recorded
outcome; revised phase dates are pending, and the prior year-end target is not a
newly confirmed schedule. No dataset or evaluation result is claimed.

## AI-assistant handoff — 2026-11-13

Owner decisions on handing the project to Claude Code. These do not change scope;
D01–D16 and both `MASTER_PLAN.md` amendments remain in force.

| ID | Accepted working decision |
| --- | --- |
| D17 | Claude Code is the sole AI assistant for the whole FYP: architecture, research, technical decisions, planning, implementation, testing, documentation and self-review. ChatGPT (coordinator) and Codex (coding agent) are no longer used; the project must not depend on their conversations. |
| D18 | Root `CLAUDE.md` holds the persistent agent instructions. Authority when sources conflict: latest explicit owner decisions (recorded here) > FYP-1 amendment > CG-002 amendment > original specification. `docs/CURRENT_STATE.md` is the live status/resume document; `docs/history/` is a non-authoritative record of past sessions and superseded proposals. |
| D19 | The repository is public (owner's choice, 2026-09-27). Raw AI transcripts are never committed; only curated, sanitised summaries. Recordings, frames of real people, personal data, credentials and weights stay out of Git. |

Recovered context (supervisor feedback relayed on 2026-09-27, the 2026-10-14
presentation requirement and the 2026-12-31 completion target) is recorded in
[CURRENT_STATE.md § 6](CURRENT_STATE.md#6-recovered-context-from-codex-prompts-was-not-in-the-repo-before-2026-11-13)
and [history/TIMELINE.md](history/TIMELINE.md). It is context, not new decisions.
Open decisions are listed in [CURRENT_STATE.md § 8](CURRENT_STATE.md#8-open-decisions).

## FYP-1 presentation date — 2026-11-13

| ID | Accepted working decision |
| --- | --- |
| D20 | The FYP-1 semester presentation is on **2026-11-24**. It will show the initial code and a working CV model detecting people and office objects on office-room footage that the team records itself (consented, staged). This replaces the pending “revised FYP-1 dates” item; 2026-12-31 remains the earlier working-system target. Scope and remaining FYP-1 deliverables for that date are to be confirmed with the owner. |
| D21 | For the 2026-11-24 presentation, CG-003 (people), CG-004 (zones/counting) and CG-005 (laptop/backpack) are delivered as **one combined perception pipeline**: a single pretrained detector pass covering person, laptop and backpack, a tracker assigning anonymous session IDs, manually configured polygon zones with visible/per-zone counts, and annotated video plus versioned structured output. Their individual FYP-1 exit criteria still apply and are reported separately. Model route and dependency installation still require owner approval. |
| D22 | Model route for the combined pipeline: **Ultralytics YOLO** (pretrained COCO detector with its built-in tracker), wrapped behind a project-owned detector/tracker interface so it can be replaced. Ultralytics is AGPL-3.0; the owner accepts this, and a matching AGPL-3.0 licence for the repository will be proposed with the README change. The exact model size and version are chosen by a measured CPU benchmark on the team's footage. |
| D23 | Approved: install CPU-only PyTorch, Ultralytics and the tracker's dependency into the `fyp` environment, pinned in `requirements.txt`, and download pretrained weights outside Git with provenance and SHA-256 recorded. Ultralytics telemetry is to be disabled. |
| D24 | Participant consent for the staged recordings has been obtained by the owner (stated 2026-11-13). Signed forms are held by the team outside the repository. Footage is recorded following `docs/dataset/RECORDING_PROTOCOL.md` and stored in `~/contextguard-data/raw/` (outside Git, owner-only permissions). |
