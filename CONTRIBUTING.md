# Contributing to ContextGuard

ContextGuard is an early-stage final-year research project. Start with the
[README](README.md), [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md) and the
governing [FYP-1 scope amendment](MASTER_PLAN.md#fyp-1-scope-amendment--2026-10-24),
which builds on the
[CG-002 amendment](MASTER_PLAN.md#scope-amendment-cg-002--2026-09-27). Read the
full master plan before proposing architecture or implementation changes. When
documents conflict, follow the authority order in [CLAUDE.md](CLAUDE.md).

## Local workflow

1. Create an isolated Python 3.10 environment using the README setup commands.
2. Create a focused branch for the change.
3. Make the change and update relevant documentation.
4. Run `python -B -m unittest discover -s tests -v` from the repository root.
5. Run `git diff --check` and review the files being committed.
6. Open a pull request describing the behavior change and verification performed.

Keep dependencies scoped to the implemented milestone and pinned in
`requirements.txt`. The test suite uses standard-library `unittest`, OpenCV/NumPy,
and Ultralytics' tracker. The real-model smoke test is skipped when weights are absent.

By contributing, you agree that your contributions are licensed under the
project's [AGPL-3.0 licence](LICENSE).

## Research and implementation standards

- Distinguish implemented, planned, experimental, and deferred functionality.
- Keep observations, inferences, explanations, and human feedback separate.
- Never treat occlusion or track loss as affirmative asset-departure evidence.
- Use cautious language such as “potential anomaly” and “requires review.”
- Label synthetic fixtures as software test data; never present them as research results.
- Keep real recordings, frames or annotated videos of people, generated reports, model weights,
  and credentials out of commits.
- Describe reproducible failures with software versions and sanitized diagnostics.

For bugs, use the issue template. Discuss substantial scope changes before starting
implementation so the research plan and acceptance criteria stay consistent.
