# Progress

> Milestone-and-task level status. One line per task. Read this to see how far the
> project has come; read `current_focus.md` to see what is happening now.

Legend: ✅ done · 🔄 in progress · 🔜 next · ⏳ pending · ⛔ blocked

---

## Milestones

| #  | Milestone            | Status   |
|----|----------------------|----------|
| 0  | Repository foundation| ✅ Done  |
| 1  | Worker Contract      | 🔜 Next  |
| 2  | Executor Contract    | ⏳       |
| 3  | ChatGPT Worker       | ⏳       |
| 4  | Gemini Worker        | ⏳       |
| 5  | Perplexity Worker    | ⏳       |
| 6  | Worker Registry      | ⏳       |
| 7  | Retry Engine         | ⏳       |
| 8  | Response Collector   | ⏳       |
| 9  | Judge (Simple)       | ⏳       |

---

## Milestone 0 — Repository foundation ✅

- [x] M0.1 Establish `.ai/` (AI-readable) and `planning/` (human-readable) split
- [x] M0.2 Write the layered contract and engineering laws
- [x] M0.3 Freeze the milestone roadmap
- [x] M0.4 Lay out the `app/` package skeleton (core/workers/executors/protocols/...)
- [x] M0.5 Define tooling (pyproject, black, isort, ruff, mypy, pytest) and scripts
- [x] M0.6 Write the bootstrap prompt + prompt library

**Outcome:** A repository that any AI agent can understand in under 10 minutes via
`.ai/` + `planning/` + the codebase map. No production code yet — that is by design.

---

## Milestone 1 — Worker Contract 🔜

Not started. Proposed first tasks (awaiting approval; see `current_focus.md`):

- [ ] M1.1 Decide response schema → ADR
- [ ] M1.2 Decide sync vs async → ADR
- [ ] M1.3 Decide failure taxonomy → ADR
- [ ] M1.4 Implement `Worker` Protocol + `BaseWorker`
- [ ] M1.5 Add shared types in `app/core/types.py`
- [ ] M1.6 Unit-test the contract with a `FakeWorker`
- [ ] M1.7 Update `codebase.md` + `changelog.md`

---

## Milestones 2–9

Tasks will be broken down when each milestone becomes active. Do not pre-plan them
in detail — the contracts decided in earlier milestones shape them.

---

## Blocked

Nothing is blocked.

---

## How to update this file

- Tick a box when a task completes; flip the milestone status when its last box ticks.
- Move a milestone from ⏳ to 🔜 when it becomes the active focus.
- Keep entries one line. Detail lives in ADRs, `architecture.md`, and `changelog.md`.
