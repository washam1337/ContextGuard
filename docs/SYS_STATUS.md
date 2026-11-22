# System-level cases SYS-01–SYS-08: status (FYP-1 deliverable 5)

**Date:** 2026-11-23. **All eight cases are PLANNED / NOT RUN.** None has passed.

The FYP-1 demo is a perception pipeline. It produces observations (visible counts,
tracks, zone membership) and makes no anomaly decision, so it cannot execute any SYS
case. A missing alert from an engine that does not exist is **not** a passing
negative case (FYP-1 amendment). The S01 perception results
([S01_RESULTS.md](S01_RESULTS.md)) are development results (D30), not SYS results.

The case definitions are those approved in the FYP-1 amendment of `MASTER_PLAN.md`.
The "related S01 footage" column shows which recordings could later supply inputs.
It is **not** a claim that the case was run.

| ID | Scenario and expected result | Status | Missing dependencies | Related S01 footage and perception observations so far |
| --- | --- | --- | --- | --- |
| SYS-01 | One visitor, allowance one → no alert | PLANNED / NOT RUN | Expected-context config (allowance); occupancy inference; temporal and anomaly engine | SC02 (one visitor). Visible persons counted exactly in 21 of 21 s with the demo model yolo11s (20 of 21 with the other three) |
| SYS-02 | Two simultaneous visitors exceed allowance beyond the duration threshold → occupancy violation | PLANNED / NOT RUN | As SYS-01, plus a duration threshold with defined start/reset | SC03 (both inside ~12 s), SC04 (~14 s). Two people counted in 32 of 33 labelled two-person seconds (all models) |
| SYS-03 | Laptop exits with removal permitted → no prohibited-removal alert | PLANNED / NOT RUN | Registered-asset and permission config; asset-state inference with affirmative departure criteria; anomaly engine | SC05 (laptop carried out). The laptop leaves `desk_area` at ~14 s; it is not detected while carried |
| SYS-04 | Laptop exits with removal prohibited → incident and evidence clip | PLANNED / NOT RUN | As SYS-03, plus evidence-clip extraction and an incident record | SC05 (same footage, different permission) |
| SYS-05 | Laptop temporarily disappears due to occlusion → no confirmed removal | PLANNED / NOT RUN | Asset-state inference that separates occlusion from departure; temporal reasoning | SC06 (hidden ~12–17 s; reappears). Perception shows the same "laptop gone from desk" signal as SC05, so this case depends entirely on the planned reasoning |
| SYS-06 | Laptop removal permission unknown → unresolved status | PLANNED / NOT RUN | Permission model with `unknown` ≠ authorised; anomaly engine | SC05 |
| SYS-07 | Brief visitor-count exceedance → no persistent violation | PLANNED / NOT RUN | Duration threshold and brief/persistent semantics | **No suitable footage:** SC04's second visitor stayed ~14 s, not briefly (D29). A new recording would be needed |
| SYS-08 | Reviewer rejects an alert → feedback stored separately | PLANNED / NOT RUN | Incident records, review UI, feedback storage separate from predictions | None (no alerts exist) |

## Before any case is run

As the FYP-1 amendment requires, each case first needs written:
- the input session and ground truth;
- the allowance and duration threshold, including boundary and reset rules;
- the permission state;
- the affirmative departure criteria;
- the expected records and alerts;
- the evidence and feedback checks.

The actual outcome is then recorded as pass, fail or not run, together with the code
revision, configuration and artifact references.
