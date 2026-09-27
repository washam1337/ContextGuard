# Working decisions — 2026-09-27

CG-002 records user/coordinator decisions. Supervisor communication is pending;
supervisor approval is not claimed. The authoritative amendment is at the end of
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
