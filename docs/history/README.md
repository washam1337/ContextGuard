# Project history archive

This folder records **how** ContextGuard reached its current state. It is a
historical record, **not a source of active requirements**. When anything here
conflicts with the current authority hierarchy, the current hierarchy wins:

1. Latest explicit decisions by the project owner (recorded in
   [DECISIONS.md](../DECISIONS.md)).
2. [FYP-1 scope amendment, 2026-10-24](../../MASTER_PLAN.md#fyp-1-scope-amendment--2026-10-24).
3. [CG-002 scope amendment, 2026-09-27](../../MASTER_PLAN.md#scope-amendment-cg-002--2026-09-27).
4. The original specification at the top of [MASTER_PLAN.md](../../MASTER_PLAN.md).

Superseded proposals are preserved here on purpose so that later readers can see
what was considered and why it changed. Do not revive a superseded proposal
without a new, explicit owner decision.

## Contents

| Path | Purpose |
| --- | --- |
| [TIMELINE.md](TIMELINE.md) | Dated, source-referenced chronology of every known milestone, decision and repository event |
| [codex/](codex/) | Curated summaries of the five OpenAI Codex sessions that produced the repository before 2026-11-13 |
| [chatgpt/](chatgpt/README.md) | What is known about the separate ChatGPT coordination conversations (no transcripts available) |

### Codex session summaries

| Date (PKT) | Session | Tasks covered |
| --- | --- | --- |
| 2026-09-01 → 2026-09-27 | [01a05d6f](codex/2026-09-01_01a05d6f_initial-audit-CG-001A-CG-002.md) | First repository audit; CG-001A audit-gap closure; **CG-002 implementation** |
| 2026-09-01 | [01a05d76](codex/2026-09-01_01a05d76_environment-verification.md) | Python interpreter verification; `fyp` declared authoritative |
| 2026-09-27 | [01a0e3b4](codex/2026-09-27_01a0e3b4_CG-001-coordination-audit.md) | CG-001 coordinated repository/environment audit |
| 2026-09-27 | [01a0e3d0](codex/2026-09-27_01a0e3d0_github-publication.md) | Repository presentation and first GitHub publication |
| 2026-10-24 | [01a16b05](codex/2026-10-24_01a16b05_FYP-1-scope-amendment.md) | FYP-1 requirements audit, FYP-1 amendment, commit `6791c95` |

## How these records were produced

- Source: the local Codex VS Code extension transcripts in `~/.codex/sessions/`
  (five `rollout-*.jsonl` files) plus `~/.codex/session_index.jsonl` for thread
  titles. Read on 2026-11-13 by Claude Code with the owner's explicit permission.
- Each transcript was converted to readable text in temporary storage, which was
  deleted after review. User prompts and assistant messages were read in full.
  Long tool outputs (mostly re-reads of `MASTER_PLAN.md`) were truncated during
  review. The CG-002 code, tests and `requirements.txt` written in the transcripts
  were verified **byte-identical** to the committed files, and the files created
  during publication were matched against commit `e931d52`.
- Not reviewed: system/developer prompts injected by the Codex extension (tool
  instructions, not project content) and the model's internal reasoning records.
- Summaries were cross-checked against Git history, the reflog and the current
  files. Where a transcript and the repository disagree, the summary says so.

## Sanitisation policy

- **Raw `.jsonl` transcripts are never committed.** This repository is public.
  The raw files stay on the owner's machine in `~/.codex/sessions/`.
- Personal email addresses, account identifiers, tokens and credential material
  are omitted. No secrets were found in the transcripts; one university email
  address and one personal email address appear in the raw files and are
  deliberately not reproduced here.
- Session IDs, timestamps, commit hashes and file paths are retained because they
  are the evidence needed to trace history.
- Machine-local paths under the owner's home directory are kept only where they
  are already part of the documented project setup (the `fyp` interpreter path).

## Summary template

Every session summary uses these sections:

1. **Source** — session ID, transcript filename, thread title, dates, Codex version and model as recorded.
2. **Context** — what the owner/coordinator asked, with important prompt wording preserved.
3. **What was done** — actions, files touched, commands.
4. **Findings and results** — verified facts and test outcomes.
5. **Decisions** — decisions made or recorded, with links to `D`-numbers.
6. **Proposals, rejected alternatives and superseded content** — and what superseded them.
7. **Open items at the end of the session.**
8. **Status today** — whether the session's outputs are still current.

## Known gaps in the historical record

See [TIMELINE.md § Gaps](TIMELINE.md#gaps-in-the-record). The most important are:
the ChatGPT coordination conversations themselves, the origin of the original
specification, the outcome of the 2026-10-14 presentation, and the supervisor's
identity and any written feedback.
