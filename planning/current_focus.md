# Current Focus

> The single source of truth for **what is being worked on right now**.
> An AI agent reads this first (after the `.ai/` context files) to know where to
> pick up. Update this at the end of every task.

---

## Active Milestone

**Milestone 1 — Worker Contract**

## Active Task

**None yet.** Milestone 0 (this repository restructure) was just completed. The
first task of Milestone 1 has not been opened.

## Next Action (proposed, awaiting approval)

Open Milestone 1 by defining the abstract `Worker` contract and its supporting
data types in `app/workers/`. Specifically:

1. Decide the **response schema** — propose a typed `WorkerResponse` (status, text,
   provenance, latency) rather than a bare string. Record as **ADR-002**.
2. Decide **sync vs async** — propose **async from day one** (concurrency is core
   to the vision). Record as **ADR-003**.
3. Decide the **failure model** — propose a `WorkerError` hierarchy splitting
   retryable from terminal. Record as **ADR-004**.
4. Implement the `Worker` Protocol and a `BaseWorker` ABC with the lifecycle
   (`start` / `send` / `stop`).
5. Add unit tests for the contract using a `FakeWorker` that satisfies the
   protocol.

Nothing here is started. It is the proposed plan for the next session.

## Blocked / Waiting

- Nothing is currently blocked. The four open design questions in
  `.ai/PROJECT_CONTEXT.md` need decisions before code lands.

## Just Finished

**Milestone 0 — Repository foundation.** Established the `.ai/` (AI-readable) and
`planning/` (human-readable) split, the layered contract, the engineering laws, the
frozen roadmap, and an empty but correctly-shaped `app/` package. See
`changelog.md` entry `[0.1.0]`.

---

## How to update this file

- When a task starts: move it from "Next Action" to "Active Task".
- When a task finishes: move it to "Just Finished" (keep only the latest), update
  `progress.md`, and write the next proposed action.
- Keep this file short. Detail lives in `context.md`, `architecture.md`, and ADRs.
