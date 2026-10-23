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
