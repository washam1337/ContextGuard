# Codex session 01a16b05: FYP-1 requirements audit and scope amendment

Historical record; see [../README.md](../README.md) for authority rules.

## 1. Source

| Field | Value |
| --- | --- |
| Session ID | `01a16b05-9622-7663-8f0b-cc521bc1e5b9` |
| Transcript | `~/.codex/sessions/2026/10/24/rollout-2026-10-24T04-08-10-01a16b05-….jsonl` (not committed) |
| Thread title | “Audit FYP-1 requirements” |
| Time | 2026-10-23 23:08–23:18Z (2026-10-24 04:08–04:18 PKT), five turns. A content-free thread-settings event on 2026-11-13. |
| Git at start | `main` at `dd765fe`, in sync with `origin/main` |
| Client / model as recorded | Codex VS Code extension `0.164.0-alpha.11.1`; `gpt-6-astra`, effort medium |

## 2. Context

Turn 1 (owner/coordinator): read `MASTER_PLAN.md`, `README.md`, `DECISIONS.md` and
`PROGRESS.md`, and inspect the code, tests and Git status. It stated:

> Our finalized FYP-1 deliverables are:
> 1. Complete system workflow diagram covering user interactions, rule configuration/storage, video processing, event reasoning, evidence clips, and feedback.
> 2. Working recorded-office-video demo with people and selected office-object detection/tracking, zones, and people counting.
> 3. Structured detections/tracks with timestamps, IDs, boxes, confidence, zones, and occupancy counts.
> 4. Dataset and pretrained-model documentation.
> 5. Test cases and honest evaluation outcomes, including SYS-01 through SYS-08.
> 6. Updated architecture, milestones, and development roadmap.
>
> Demo pipeline: recorded video -> detection -> tracking -> zones/counting -> annotated video + structured output.
> Proposed milestones: CG-003 person detection/tracking; CG-004 counting/zones; CG-005 office-object detection/tracking; CG-006 demo integration/testing/evaluation.

Codex was told to compare these with the repo, preserve completed CG-002, edit
nothing, and return an audit plus proposed `MASTER_PLAN.md` updates.

## 3–4. Audit findings (turn 1)

- 10 tests passed in 1.937 s. OpenCV 5.0.0 (package 5.0.0.93), NumPy 2.2.6,
  `pip check` clean. Bare `python` was Conda base.
- **Gap per deliverable:**
  - existing diagrams did not trace configuration → storage → reasoning → evidence → feedback with implementation boundaries;
  - no detection, tracking, zones, counting or annotated video;
  - only the inspection schema existed, with no frame-level observation contract;
  - no dataset manifest, model or weights docs;
  - **SYS-01–SYS-08 were not defined anywhere**, and Codex refused to invent them;
  - CG-003–CG-006 were not recorded.
- **Inconsistencies:**
  - the plan's development order put object tracking before zones and required reasoning, anomaly decisions and evidence in the first slice, conflicting with the FYP-1 pipeline;
  - there was no FYP-1-versus-full-system distinction;
  - `HANDOFF.md`'s pilot-only CG-003 should become a prerequisite inside CG-003;
  - “selected office objects” should stay laptop + backpack;
  - the 10-14 date had passed with no outcome recorded;
  - HANDOFF's “untracked/no commits” wording was historical.
- **Technical risks:**
  - timing basis and video/output alignment;
  - counting semantics (simultaneous occupancy, boundaries, overlap, track confirmation, lost tracks; visible ≠ occupancy);
  - tracking ID switches and occlusion; track ID ≠ asset identity; disappearance ≠ departure;
  - reproducibility (model/tracker versions, class mapping, weights checksum, licensing, thresholds, resolution, CPU throughput); no real-time claim;
  - evaluation (consented footage, ground truth, tuning/evaluation separation, thresholds, failure reporting);
  - environment (bare `python` is base).
- Proposed an **append-only FYP-1 amendment** with six points, all adopted.

## 3. What was done (turns 2–5)

- **Turn 2** (approval, wording preserved): proceed with an append-only amendment that
  “supersedes conflicting implementation order, demo acceptance criteria, and
  milestone definitions for the current phase, without changing the overall
  expected-vs-observed research objective.” Keep laptop and backpack. Document
  detection is experimental and feasibility-dependent. Restricted zones are manually
  configured polygons. The SYS definitions were supplied verbatim:

  | ID | Definition supplied by owner |
  | --- | --- |
  | SYS-01 | One visitor, allowance one, no alert. |
  | SYS-02 | Two simultaneous visitors exceed allowance beyond duration threshold, occupancy violation. |
  | SYS-03 | Laptop exits with removal permitted, no prohibited-removal alert. |
  | SYS-04 | Laptop exits with removal prohibited, incident and evidence clip. |
  | SYS-05 | Laptop temporarily disappears due to occlusion, no confirmed removal. |
  | SYS-06 | Laptop removal permission unknown, unresolved status. |
  | SYS-07 | Brief visitor-count exceedance, no persistent violation. |
  | SYS-08 | Reviewer rejects an alert, feedback stored separately. |

  They are to be marked as planned system-level cases, separate from the CG-002 tests,
  with frame-level observation requirements and visible count ≠ inferred occupancy.
  Update DECISIONS and PROGRESS; no code; no invented results; no commit.

  Codex appended “FYP-1 scope amendment — 2026-10-24” (162 lines). It added
  D10–D16 and replaced one outdated sentence in DECISIONS (the CG-002 amendment is
  now described as “historical”). It added the “FYP-1 scope approved; implementation
  pending” section to PROGRESS.
  Verification script: the old file is a byte prefix of the new; only the 3 files
  changed; exactly 8 `SYS-` rows marked `PLANNED / NOT RUN`. `git diff --check` clean.
  Diff: 3 files, +223/−1.
- **Turn 3:** review the diff and commit only those three files. Review found no
  inconsistencies. The commit failed: no Git author identity was configured.
- **Turn 4:** owner supplied a name and email. Codex set a **repository-local**
  Git identity and committed **`6791c95`** “docs: finalize ContextGuard FYP-1 scope and milestones”.
- **Turn 5:** `git push origin main` failed twice (sandbox DNS, then no HTTPS
  credentials: “could not read Username”). Codex reported the commit as local and unpushed.

## 5. Decisions

D10–D16 in [DECISIONS.md](../../DECISIONS.md), still current.

## 6. Superseded content

- The original §“Required development order” and “First runnable vertical slice”
  stop governing the current phase.
- The pilot-only CG-003 from `HANDOFF.md` is absorbed into CG-003.
- The earlier pending item “later milestone acceptance criteria” is resolved.

## 7. Open items at the end

Push pending. Also open: model/tracker selection; observation and configuration
schemas; polygon, count and occupancy policies; duration-threshold semantics; timing
validation; affirmative departure criteria; numerical targets; consent; pilot
collection; asset positions; supervisor communication; revised dates.

## 8. Status today

`origin/main` is now `6791c95` and CI run **40039326735** (2026-10-23 23:22Z)
passed. How it was pushed is not recorded in any transcript; it presumably happened
outside the Codex sandbox. Everything else in §7 is still open.
