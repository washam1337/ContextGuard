# Codex session 01a0e3b4: CG-001 coordinated repository and environment audit

Historical record; see [../README.md](../README.md) for authority rules.

## 1. Source

| Field | Value |
| --- | --- |
| Session ID | `01a0e3b4-4dfe-7042-a808-fbe1c09377ca` |
| Transcript | `~/.codex/sessions/2026/09/27/rollout-2026-09-27T21-30-39-01a0e3b4-….jsonl` (not committed) |
| Thread title | “Audit repository and environment” |
| Time | 2026-09-27 16:30–16:32Z (21:30–21:32 PKT), one turn |
| Client / model as recorded | Codex VS Code extension `0.155.0-alpha.16.3`; `gpt-6-astra`, effort high |

## 2. Context

This was the **first task relayed from the ChatGPT coordination conversation**.
The prompt says: “I am coordinating this project with ChatGPT in a separate
conversation and will relay your findings. Do not assume access to that conversation.”

“Confirmed project facts” supplied in the prompt (preserved, because several were
not written into the repository until 2026-11-13):

- Completion target: **December 31, 2026**.
- Next presentation: **October 14, 2026**, “requiring a concrete dataset solution and development roadmap.”
- **Supervisor feedback: “refine the use case and clearly specify the behaviours/anomalies to detect.”**
- Reported repository contents: master plan and VS Code settings only.
- Configured interpreter: `/home/w4shm1337/miniconda3/envs/fyp/bin/python`.
- “A university faculty member’s individual office is a proposed scope refinement, not yet an accepted requirement.”

The task was a read-only audit reporting nine items: root/tree, Git state without
initialising, plan filename and SHA-256, interpreter, package versions/imports,
CPU/RAM/GPU (separating unavailable tools from unavailable hardware), existing
code/tests, plan ambiguities that affect dataset design, and the smallest
recorded-video feasibility task with inputs and acceptance criteria. Output
title: “CG-001 RESULTS”.

## 3. What was done

Codex read the plan, listed files, checked Git and ran import checks under a
Python audit hook that blocked filesystem writes. It also ran an in-memory
NumPy→OpenCV smoke test, read the OpenCV build information and ran `pip check`.

## 4. Findings

- Root `/home/w4shm1337/fyp`. Files: `MASTER_PLAN.md`, `.vscode/settings.json`,
  and empty `.agents/` and `.codex/`. No `AGENTS.md` anywhere.
- **Git initialised on `master` with no commits**; both files untracked.
- `MASTER_PLAN.md` SHA-256 `9e161cd5…26af6c1`, 1,763 lines.
- `fyp` interpreter is Python 3.10.21 (GCC 14.3.0) with Conda metadata. Bare
  `python` resolves to Conda base.
- OpenCV 5.0.0.93 and NumPy 2.2.6 import. PyTorch, Ultralytics, FastAPI,
  pytest, torchvision, Pydantic, SciPy and pandas are missing. OpenCV
  **FFmpeg enabled, GStreamer disabled**. `pip check` clean.
- i5-1135G7, 4 cores / 8 threads, 7.6 GiB RAM, 2 GiB swap. `nvidia-smi`, `nvcc`,
  `lspci`, `/dev/dxg` and `/dev/dri` are all absent, so GPU/CUDA is “not established”.
- All application modules PLANNED; no code.

### Ambiguities identified

The ambiguities are as Codex reported them. The italic *Resolved / Partly resolved /
Still open* notes are **Claude Code's 2026-11-13 assessment** against the later
amendments; they are not part of the transcript.

- **Use case:** faculty office was only a proposal. *Resolved in CG-002.*
- **Detection definitions:** entry vs occupancy count, staff vs visitors, pickup,
  removal, return, occlusion, persistence thresholds, insufficient evidence.
  *Partly resolved* (occupant excluded, simultaneous occupancy, occlusion ≠
  departure); thresholds and departure criteria **still open**.
- **Identity:** named-person examples have no mechanism linking anonymous tracks to
  authorisation, and face recognition is excluded. *Resolved by scoping*: anonymous
  session IDs; the two current anomalies use a session visitor allowance and per-asset
  removal permissions, so neither needs to know who a person is.
- **Dataset:** access, participants, counts, assets, layout, annotation rules, splits,
  consent and retention all unspecified. *Assets resolved; the rest still open.*
- **Contracts/evaluation:** schemas are untyped sketches; matching tolerances and
  thresholds undecided. *Still open* (observation schema required by FYP-1, not yet defined).
- **Scope consistency:** audio is optional but appears as a milestone exit criterion.
  *Resolved:* audio/accessibility DEFERRED.
- **Schedule:** phases had no dates. *Partly resolved*: 10-14 and year-end; revised FYP-1 dates pending.

## 5. Decisions

None recorded in this session. The faculty-office refinement was still a proposal.

## 6. Proposal (superseded)

**“CG-002: recorded-video feasibility pilot”** (proposal only):
- one fixed camera, one consenting actor, one visible asset, desk/exit zones;
- two short recordings: asset carried out, and asset moved and returned;
- the removal recording replayed under “removal permitted” and “asset must remain” contexts.

Proposed acceptance criteria:
- CPU completion with runtime reported;
- tracks and asset transitions matching references within a pre-declared tolerance;
- identical observations giving *normal* vs *potential anomaly* when only authorisation changes;
- no alert for move-and-return;
- saved events, decisions, explanations and playable clips with identifiers;
- reproducible deterministic tests.

**Superseded the same day.** The coordinator assigned CG-002 as recorded-video
*inspection* instead (session 01a05d6f, Task C). Claude Code's note: the idea of
replaying identical observations under different permissions closely matches the
later SYS-03/SYS-04/SYS-06 cases in the FYP-1 amendment, but no record links the two.

## 7. Open items

Inputs needed: recordings, asset choice, zone coordinates, timestamped reference
annotations, expected contexts, and an agreed CPU detector/tracker with versioned weights.

## 8. Status today

Facts current except the Git state: `main` now has published history (see
`git log`), plus the orphan `local-preparation` branch. The recovered supervisor feedback, presentation requirement
and 2026-12-31 date are now recorded in [../TIMELINE.md](../TIMELINE.md) and
[../../CURRENT_STATE.md](../../CURRENT_STATE.md).
