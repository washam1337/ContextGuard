# ContextGuard timeline

Historical record only; see [README.md](README.md) for authority rules.
Times are Pakistan Standard Time (PKT, UTC+5) unless marked `Z` (UTC). Git
commit times are as recorded by Git. "Source" names the evidence for each entry.

## Chronology

| When | Event | Source | Still current? |
| --- | --- | --- | --- |
| Before 2026-09-01 | The original project specification was written as *“ContextGuard — Master FYP Project Handoff for Claude”* in an earlier AI conversation that is not available, then adapted into `MASTER_PLAN.md` “for ChatGPT/Codex and other coding agents”. That version is 1,763 lines, 68,258 bytes, SHA-256 `9e161cd5…26af6c1`. | `MASTER_PLAN.md` header; CG-001/CG-001A hash checks | The text is preserved byte for byte. As scope it is historical; see the amendments. |
| Before 2026-09-01 | Conda env `fyp` (Python 3.10.21) already contained OpenCV 5.0.0.93, NumPy 2.2.6, ONNX Runtime 1.23.2, TensorFlow 2.21.0, Keras 3.12.4, tflite-runtime 2.14.0, Jupyter and matplotlib. Conda `base` was Python 3.14.7. Why these packages were installed is unrecorded. | Session [01a05d6f](codex/2026-09-01_01a05d6f_initial-audit-CG-001A-CG-002.md) audit | Yes. Package set unchanged on 2026-11-13. |
| 2026-09-01 14:48Z | **First repository audit** (unnumbered). The repo held only `MASTER_PLAN.md` and `.vscode/settings.json`; `.git` was empty and invalid. Codex proposed a first full-reasoning vertical slice. | Session 01a05d6f | Superseded (see FYP-1 amendment). |
| 2026-09-01 14:54Z | **Environment verification.** Owner declared `/home/w4shm1337/miniconda3/envs/fyp/bin/python` the authoritative interpreter; Conda base is not to be used. | Session [01a05d76](codex/2026-09-01_01a05d76_environment-verification.md) | Yes (D09). |
| 2026-09-01 → 2026-09-27 | Git was initialised on branch `master` with no commits. `.vscode/settings.json` gained `python.defaultInterpreterPath`. Exact dates are unknown. | Observed by the 2026-09-27 audits | Yes (settings file is git-ignored). |
| 2026-09-27 21:30 | **CG-001 coordinated audit.** First task relayed from the separate ChatGPT coordination conversation. It recorded the supervisor feedback, the 2026-10-14 presentation requirement and the 2026-12-31 completion target (see [Recovered context](#recovered-context-not-recorded-elsewhere-before-2026-11-13)). Codex proposed CG-002 as a *recorded-video feasibility pilot*. | Session [01a0e3b4](codex/2026-09-27_01a0e3b4_CG-001-coordination-audit.md) | The feasibility-pilot meaning of CG-002 is superseded. |
| 2026-09-27 21:33 | **CG-001A audit-gap closure.** The `MASTER_PLAN.md` hash matched the coordinator's copy. The interpreter setting was confirmed, and the hardware recorded: i5-1135G7, 8 logical CPUs, 7.63 GiB RAM, GPU availability undemonstrated. The coordinator corrected the earlier audit: modules are PLANNED; dependencies are chosen per milestone. | Session 01a05d6f | Yes. |
| 2026-09-27 21:44–21:50 | **CG-002 implemented.** Codex appended the CG-002 scope amendment and created `scripts/inspect_video.py`, `tests/test_inspect_video.py` (10 tests, passed in 2.088 s), `requirements.txt`, a minimal README, `docs/DECISIONS.md` (D01–D09), `docs/PROGRESS.md` and `docs/HANDOFF.md`. It proposed CG-003 as *pilot capture and placement review*. | Session 01a05d6f | Code current. The pilot-only meaning of CG-003 is superseded. |
| 2026-09-27 22:01–22:17 | **Public GitHub publication.** Owner asked for a “very presentable” push and chose a **public** repo. Codex rewrote the README and added the banner, `CONTRIBUTING.md`, `docs/VIDEO_INSPECTION.md`, issue/PR templates, CI, `.gitignore` and `.gitattributes`. Local commit `e931d52` (22:10). Owner created the empty GitHub repo by hand. Codex published through the GitHub API: `f950ef5` (22:13, `.gitattributes`), then `dd765fe` (22:16, same tree as `e931d52`). The local branch was renamed `local-preparation`; `main` tracks `origin/main`. CI run 36336320051 passed. | Session [01a0e3d0](codex/2026-09-27_01a0e3d0_github-publication.md); Git reflog | Yes. `local-preparation` still exists (unpushed, identical tree). |
| 2026-10-14 | Planned FYP presentation, which required “a concrete dataset solution and development roadmap”. **Outcome not recorded anywhere.** | CG-001 prompt; D08 | Unknown. |
| 2026-10-24 04:08 | **FYP-1 requirements audit.** Owner supplied six finalised deliverables, the demo pipeline and milestones CG-003 to CG-006. Codex found gaps: SYS-01–08 were undefined, the plan's vertical slice conflicted with the new pipeline, and the observation contract was missing. | Session [01a16b05](codex/2026-10-24_01a16b05_FYP-1-scope-amendment.md) | Yes. |
| 2026-10-24 04:11–04:18 | **FYP-1 amendment.** Owner approved an append-only amendment with SYS-01–SYS-08 definitions. `MASTER_PLAN.md`, `DECISIONS.md` (D10–D16) and `PROGRESS.md` were updated and committed as `6791c95` after a repository-local Git identity was set. The push from Codex failed (no credentials in the sandbox). | Session 01a16b05 | Yes. |
| 2026-10-24 04:22 | `6791c95` reached `origin/main` and CI run 40039326735 passed. The push itself is not recorded in any transcript; it presumably happened outside the Codex sandbox. | GitHub Actions; `git ls-remote` | Yes. |
| 2026-11-13 | **Claude Code becomes the sole AI assistant.** ChatGPT and Codex are no longer used. Claude Code ran a read-only audit (10/10 tests pass, CI green, `MASTER_PLAN.md` confirmed append-only). With owner approval it then read the five Codex transcripts and created `CLAUDE.md`, this history archive and `docs/CURRENT_STATE.md`. | This archive; [DECISIONS.md](../DECISIONS.md) D17–D19 | Yes. |

## Milestone-name history

The meaning of the CG numbers changed twice. Current meanings are in the FYP-1 amendment.

| ID | Earlier proposed meaning | Proposed in | Current meaning |
| --- | --- | --- | --- |
| CG-001 | — | — | Repository and environment audit (CG-001A: follow-up gap closure) |
| CG-002 | Recorded-video **feasibility pilot**: one actor and one asset, desk/exit zones, permitted vs prohibited context replay, structured events and evidence clips | CG-001 results, 2026-09-27 | **Recorded-video inspection**, as assigned by the coordinator on 2026-09-27. Complete. |
| CG-003 | Staged pilot capture and camera-placement review only | CG-002 handoff, 2026-09-27 | Person detection/tracking, which *includes* the pilot and placement review as prerequisites (FYP-1 amendment) |
| CG-004–006 | — | — | Counting/zones; office-object detection/tracking; integration/testing/evaluation |

## Recovered context not recorded elsewhere before 2026-11-13

These facts appear in Codex prompts relayed from the coordination conversation
but were not written into repository documents before this archive:

- **Supervisor feedback (as relayed on 2026-09-27):** “refine the use case and
  clearly specify the behaviours/anomalies to detect.” The CG-002 narrowing to one
  faculty office with two defined anomalies is the response to this feedback.
- **2026-10-14 presentation requirement:** “a concrete dataset solution and
  development roadmap.”
- **Completion target:** December 31, 2026, recorded in the repo only as “year-end 2026”.
- On 2026-09-27 the faculty-office scope was first described as “a proposed
  scope refinement, not yet an accepted requirement”. It was accepted later that day in CG-002.

## Gaps in the record

| Missing item | Status |
| --- | --- |
| ChatGPT coordination conversations (reasoning behind CG-002 and FYP-1 decisions) | Not available on this machine. Only their outputs, relayed as Codex prompts, survive. See [chatgpt/README.md](chatgpt/README.md). |
| The source conversation of *“Master FYP Project Handoff for Claude”* | Unavailable. The document itself survives byte for byte in `MASTER_PLAN.md`. |
| Outcome of the 2026-10-14 presentation | Not recorded. Ask the owner. |
| Supervisor identity, written feedback beyond the one sentence above, and whether the scope refinement was communicated | Not recorded. Supervisor approval must not be assumed. |
| Second team member (D08 says “two students”) and the division of work | Not recorded. |
| University FYP-1 deadline, deliverable format and grading rubric | Not recorded. |
| Why TensorFlow, Keras, tflite-runtime and ONNX Runtime are in `fyp` | Not recorded; they predate all Codex work. |
| Exact dates of `git init` and the VS Code interpreter setting | Not recorded. |
| Whether any real pilot footage exists | None found in the repository or ignored folders on 2026-09-01, 2026-09-27, 2026-10-24 or 2026-11-13. The CG-002 sentence “existing source footage was not modified or deleted” is a safety statement; the audits that day found no media, so it does not imply that real footage existed. Owner should confirm whether any footage exists outside the repository. |
