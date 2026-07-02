# Progress

> Milestone-and-task level status. One line per task. Read this to see how far the
> project has come; read `current_focus.md` to see what is happening now.

Legend: ✅ done · 🔄 in progress · 🔜 next · ⏳ pending · ⛔ blocked

---

## Milestones

| #  | Milestone            | Status   |
|----|----------------------|----------|
| 0  | Repository foundation| ✅ Done  |
| 1  | Worker Contract      | ✅ Done  |
| 2  | Executor Contract    | 🔜 Next  |
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

## Milestone 1 — Worker Contract ✅

- [x] M1.1 Decide response schema → ADR-0002 (typed `Response` dataclass)
- [x] M1.2 Decide sync vs async → ADR-0003 (async-first from day one)
- [x] M1.3 Decide failure taxonomy → ADR-0004 (retryable vs terminal per layer)
- [x] M1.4 Implement `Task` (immutable dataclass in `app/core/task.py`)
- [x] M1.5 Implement `Response` + `ResponseStatus` (frozen dataclass in `app/core/response.py`)
- [x] M1.6 Implement `BaseExecutor` + error hierarchy (generic, `app/executors/base_executor.py`)
- [x] M1.7 Implement `BaseWorker` + error hierarchy + Template Method `send()` (`app/workers/base_worker.py`)
- [x] M1.8 Unit-test all four contracts (42 tests, 99% coverage, all passing)
- [x] M1.9 Update planning docs + changelog

**Outcome:** The four core contracts are defined, tested, and documented. Any concrete
worker or executor now has a clear, typed interface to implement.

### Milestone 1 retrospective — four questions

**What problem did we solve?**
CouncilOS had no code contracts. Without a shared `Task`, `Response`, `BaseWorker`,
and `BaseExecutor`, no two modules could interoperate. We now have the interfaces
that every future worker (ChatGPT, Gemini, Perplexity), executor (HTTP, browser),
and consumer (collector, judge) will plug into — with provenance, timing, and
typed error classification built in from the start.

**What assumptions did we make?**
1. A typed `Response` (not a bare string) is the right shape. This adds a small
   amount of ceremony but buys provenance and latency for free. If responses need
   rich structure later (citations, tokens, model version), we extend the
   dataclass — no contract rewrite.
2. Async-first is worth the slight complexity cost even during single-worker
   development (M3–M5), because fan-out in M6+ is the core vision and a sync-to-
   async migration would touch every test and implementation.
3. The error taxonomy (retryable vs terminal) can be correctly classified at the
   executor/worker level — i.e., the layer that sees the transport detail knows
   best whether a failure is transient.
4. `BaseWorker.send()` wrapping `WorkerError` → FAILED Response is acceptable,
   even though the future Retry Engine (M7) will need to decide whether to call
   `send()` or `_send()`. That bridge is deferred to M7 when the usage pattern is
   known (rule of three).

**What could break this in the future?**
1. If `Response` needs rich structured fields (citations, token counts, model
   version), the frozen dataclass grows. This is fine — dataclasses are
   extensible — but any consumer that pattern-matches on `Response` fields will
   need updating. Mitigated by the fact that all consumers are inside our repo.
2. If a worker needs to return *multiple* responses per task (streaming chunks),
   the current `str` return from `_send` won't fit. This would require either
   a new `StreamingWorker` sub-contract or an `AsyncIterator` return type. Not
   anticipated for the frozen core (M0–M9) but possible post-M9.
3. If the Retry Engine (M7) decides to bypass `send()` and call `_send()` directly,
   the Template Method timing/provenance wrapper is skipped. The Retry Engine must
   rebuild the Response itself — duplicating that bookkeeping. This tradeoff is
   documented in ADR-0004.
4. Python 3.14 was used for testing. `slots=True` requires 3.10+ and `str |
   None` requires 3.10+. These are enforced in `pyproject.toml` but would break
   if someone tried to run on 3.9.

**What should the next milestone build on?**
Milestone 2 (Executor Contract) should build on:
- The `BaseExecutor` generic interface defined here (extend if M2 uncovers gaps,
  but do not redesign it).
- The error taxonomy: the M2 concrete executor families (HTTP, browser) must raise
  `RetryableExecutorError` / `TerminalExecutorError` appropriately.
- The async-first convention: all M2 executor implementations and tests must be
  async, following the patterns established in M1 tests.

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
