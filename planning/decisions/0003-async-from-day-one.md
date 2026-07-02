# ADR-0003: Async-first contract from day one

- **Status**: Accepted
- **Date**: 2026-07-02

## Context
CouncilOS's core vision is concurrent fan-out: send the same prompt to multiple
workers simultaneously and reconcile the results. If the worker contract is
synchronous, adding concurrency later means rewriting every interface, every
test, and every concrete worker. That's a high-cost migration with high regression
risk.

## Decision
All worker and executor contracts are async: `send`, `_send`, `execute`, `_execute`,
`start`, `stop` are `async def`. Lifecycle is via `__aenter__`/`__aexit__` (standard
Python resource management). `pytest-asyncio` with `asyncio_mode = auto` runs async
tests transparently.

## Consequences
- **Positive:** Fan-out in Milestone 6+ is a natural `asyncio.gather` — no
  contract rewrite needed. Thread-safety concerns don't arise (single event loop).
- **Negative:** Slight learning curve for contributors unfamiliar with async
  Python. All test helpers must be async too.
- **Neutral:** The cost of async is zero for single-worker use (M3–M5 development)
  since the event loop serializes naturally.

## Alternatives considered
- **Sync now, add async later.** Rejected: every downstream consumer (protocols,
  core, tests) would need a dual-mode or rewrite. Async-first is cheaper long-term.
- **Callback / event-driven.** Rejected: harder to compose and reason about than
  the coroutine model. `async/await` is the Python mainstream choice (3.10+).
