# ChatGPT coordination: what is known

Historical record; see [../README.md](../README.md) for authority rules.

The owner used ChatGPT, in a separate conversation, as architect, planner, research
and documentation assistant, and reviewer of Codex reports. The owner relayed
instructions and results by hand. Prompts call this role “the coordinator” or
“the coordinating conversation”. The first explicit mention in a Codex prompt is
2026-09-27 (CG-001) and the last coordinated task is 2026-10-24. The
`MASTER_PLAN.md` header shows the specification had already been adapted “for
ChatGPT/Codex” before 2026-09-01, so the collaboration may have started earlier.

**No ChatGPT transcripts are available**, either on this machine or in the
repository. As of 2026-11-13 ChatGPT is no longer used (see D17 in
[DECISIONS.md](../../DECISIONS.md)), and the project must not depend on those
conversations.

## What survives

The coordinator's outputs survive only where they were relayed into Codex prompts
and then written into the repository:

| Coordinator output | Where it survives |
| --- | --- |
| Coordinated-audit brief, with the supervisor feedback, presentation requirement and completion date | [codex/2026-09-27_01a0e3b4](../codex/2026-09-27_01a0e3b4_CG-001-coordination-audit.md); [TIMELINE.md](../TIMELINE.md) |
| CG-001A corrections (modules PLANNED; audio and learned temporal optional; per-milestone dependencies; missing detection ≠ departure) | [codex/2026-09-01_01a05d6f](../codex/2026-09-01_01a05d6f_initial-audit-CG-001A-CG-002.md) Task B |
| The *coordinating copy* of `MASTER_PLAN.md` (SHA-256 `9e161cd5…26af6c1`) | Byte for byte, the first 68,258 bytes of `MASTER_PLAN.md` |
| CG-002 accepted working decisions | `MASTER_PLAN.md` CG-002 amendment; D01–D09 |
| FYP-1 deliverables, pipeline, milestones and SYS-01–08 definitions | `MASTER_PLAN.md` FYP-1 amendment; D10–D16 |

## What is lost

- The reasoning, alternatives and literature discussion behind the CG-002 and
  FYP-1 decisions. Only the decisions themselves survive.
- Any discussion of the 2026-10-14 presentation and its outcome.
- The conversation that produced the original *“Master FYP Project Handoff for Claude”*.

“User/coordinator approval” in the amendments means the owner accepted the decision.
It is **not** supervisor approval.
