# Changelog

> Notable changes to CouncilOS, newest first. Based on [Keep a Changelog];
> versions follow [Semantic Versioning].
>
> Each entry should let a reader answer "what changed and why" without reading the
> diff. Pair every implementation commit with a line here.

[Keep a Changelog]: https://keepachangelog.com/en/1.1.0/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html

---

## [Unreleased]

_(Nothing staged yet. Milestone 1 work will appear here.)_

---

## [0.1.0] — 2026-07-01 — "Repository Foundation"

### Context
This release restructures CouncilOS from an early debate-prototype layout into a
documentation-first, contract-driven project. The old `app/agents` +
`app/automation` (advocate/critic/judge + ChatGPT DOM client) code is **removed**;
it is recoverable from git history but is **superseded** by the
worker/executor/protocol/core layering introduced here.

### Added — `.ai/` (AI-readable)
- `AGENT.md`: the AI implementation engineer's charter — startup sequence,
  operating principles, the 10-minute rule.
- `PROJECT_CONTEXT.md`: executive summary (what/why/architecture/vision/constraints).
- `DEVELOPMENT_RULES.md`: ten permanent engineering laws.
- `CODING_STANDARDS.md`: formatting, typing, async, tests, naming conventions.
- `PROMPTS/`: reusable `bootstrap`, `implementation`, `review`, `debug` prompts.

### Added — `planning/` (human-readable)
- `current_focus.md`, `context.md`, `progress.md`: live project state.
- `architecture.md`: the layered contract (Executors/Workers/Protocols/Core) and
  dependency direction.
- `codebase.md`: a module map with single-sentence responsibilities.
- `roadmap.md`: the **frozen** milestone sequence (M0–M9).
- `testing.md`: the testing contract (unit/integration/browser split, markers).
- `research_notes.md`: preserved browser-automation findings (profiles,
  anti-detection, DOM stream-stabilization) carried over to feed M3.
- `decisions/0001-repository-foundation-and-layered-contract.md`: the founding ADR.

### Added — project skeleton
- `app/` package skeleton: `core/`, `workers/`, `executors/`, `protocols/`,
  `storage/`, `utils/`, `config/`, `cli/` (empty, awaiting M1+).
- `tests/` skeleton: `unit/`, `integration/`, `browser/`, `fixtures/`.
- `scripts/` shell entry points: `setup.sh`, `run.sh`, `test.sh`, `format.sh`.
- `pyproject.toml` (modern build config; replaces `setup.py`/`requirements.txt`).
- `.env.example`, refreshed `README.md`, refreshed `.gitignore`.

### Removed
- Pre-restructure `app/` (agents/automation/judges/memory/protocols/retrieval/utils).
- `setup.py`, `requirements.txt` (superseded by `pyproject.toml`).
- Old `planning/` docs (architecture/roadmap/decisions/changelog/research_notes —
  their content lives on in the new files above; the framing is superseded).

### Design intent
The repository is now understandable from `.ai/` + `planning/` + the structure
alone, in under 10 minutes, by any model or contributor. The first production code
(Worker Contract, Milestone 1) can now begin on a clean, well-specified base.
