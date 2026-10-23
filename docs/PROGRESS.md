# Progress — 2026-09-27

CG-001/CG-001A: repository/environment audits completed. Requirements documented;
no application functionality existed at CG-002 entry. Verified interpreter:
`/home/w4shm1337/miniconda3/envs/fyp/bin/python` (3.10.21).

CG-002: scope amendment recorded; headless recorded-video inspection implemented.
Verification results are recorded in [HANDOFF.md](HANDOFF.md).

| Component | Current status |
| --- | --- |
| Recorded-video inspection command | IMPLEMENTED; synthetic software validation only |
| Module A video ingestion | PARTIAL; offline decode/inspection only, no live capture or rolling evidence buffer |
| Representative review JPEGs and inspection JSON | IMPLEMENTED; not incident evidence or structured event storage |
| Detection/tracking, zones, interaction/asset state | PLANNED |
| Structured events, session context, anomaly rules, deterministic temporal reasoning | PLANNED |
| Evidence windows/clips, explanations, dashboard/API, feedback, evaluation | PLANNED |
| Audio and accessibility workflows | DEFERRED for current build by CG-002 working decision |
| Learned temporal modelling | PLANNED as an optional proposal, not an accepted implementation commitment |
| Custom research dataset | PLANNED; no real-video results or research metrics available |

The first complete vertical slice remains unimplemented. The next proposed task is
pilot recording and placement review using this utility, followed by a separately
scoped CPU pretrained perception baseline. No models were downloaded in CG-002.

## Repository presentation — 2026-09-27

Prepared the public repository documentation: branded README, portable setup
instructions, inspection reference, contribution guidance, issue/PR templates,
and a Python 3.10 GitHub Actions workflow. Ignore rules exclude local editor
settings, credentials, recordings, model weights, and inspection outputs.
The existing 10 software tests passed again in the verified fyp environment.
This packaging work does not change the implementation milestone or research status.

## FYP-1 scope approved; implementation pending — 2026-10-24

Recorded the user/coordinator-approved [FYP-1 amendment](../MASTER_PLAN.md#fyp-1-scope-amendment--2026-10-24)
and updated working decisions. This is documentation work only; no detection,
tracking, zones, counting or reasoning code was implemented. The original master
specification and CG-002 amendment remain unchanged; CG-002 remains completed.

| Milestone/deliverable | Current status and next evidence |
| --- | --- |
| CG-002 recorded-video inspection | IMPLEMENTED; existing inspector/schema/tests preserved. Ten automated inspection tests passed during the 2026-10-24 audit using synthetic fixtures, not research recordings. |
| CG-003 person detection/tracking | PLANNED; consented pilot/placement review, CPU pretrained baseline, anonymous tracks, frame observations and annotated preview. Replaces the earlier pilot-only CG-003 proposal. |
| CG-004 counting/zones | PLANNED; manually configured polygons, visible/per-zone counts, separate occupancy semantics and boundary/track-loss validation. |
| CG-005 office-object detection/tracking | PLANNED; laptop/backpack baseline and stationary/movement/occlusion evaluation. Document detection remains EXPERIMENTAL in scope only; no prototype exists. |
| CG-006 integration/testing/evaluation | PLANNED; reproducible recorded-video demo producing annotated video and aligned structured output, with honest evaluation and limitations. |
| Complete workflow diagram and architecture | PLANNED update; must cover user configuration/storage, processing/reasoning, evidence and separately stored feedback with implementation boundaries. Existing conceptual diagrams do not complete this deliverable. |
| Dataset and pretrained-model documentation | PLANNED; no collected research dataset, selected model/weights or office-video metrics are claimed. |
| SYS-01–SYS-08 | Definitions recorded in the amendment; all PLANNED / NOT RUN. Separate from CG-002 automated tests. |
| Updated milestones and roadmap | Phase scope and exit criteria documented; detailed implementation/evaluation protocols and revised dates remain pending. |

FYP-1's executable path ends at annotated video and structured observations.
Interaction/asset state, contextual/temporal reasoning, incidents, evidence clips,
dashboard/API, feedback persistence and comparative reasoning evaluation remain
later PLANNED work. Audio/accessibility remain DEFERRED; learned temporal modelling
remains optional/proposed. Visible-person counts must not be reported as inferred
office occupancy without an explicit validated policy.

Next milestone is CG-003, beginning with consented pilot collection and camera
placement review using the preserved inspector. Pending decisions include model
selection, schema/timing and zone/count policies, occupancy duration semantics,
affirmative departure evidence and quantitative acceptance targets. Supervisor
communication remains pending; approval and past presentation outcomes are not
asserted. No milestone implementation or system-level pass is claimed here.
