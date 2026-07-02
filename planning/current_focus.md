# Current Focus

> The single source of truth for **what is being worked on right now**.
> An AI agent reads this first (after the `.ai/` context files) to know where to
> pick up. Update this at the end of every task.

---

## Active Milestone

**Milestone 2 — Executor Contract** 🔜

## Active Task

**None yet.** Milestone 1 (Worker Contract) just completed. M2 has not been opened.

## Next Action (proposed, awaiting approval)

Open Milestone 2 by defining concrete executor families that implement the
`BaseExecutor` contract from `app/executors/base_executor.py`. Specifically:

1. Define the `HttpApiExecutor` — a generic executor for REST/SDK model calls.
   What request type does it use? (url, method, body? Or a wrapped `ApiRequest`?)
2. Define the `BrowserExecutor` — an executor that drives a Playwright page.
   Request type: prompt + selectors.
3. Build on the error taxonomy: both families must raise `RetryableExecutorError`
   or `TerminalExecutorError` appropriately.
4. Write unit tests with fake HTTP and fake browser backends.
5. Update `codebase.md` + `changelog.md`.

Nothing here is started. It is the proposed plan for the next session.

## Blocked / Waiting

- Nothing is currently blocked. The four open design questions from
  `.ai/PROJECT_CONTEXT.md` were resolved by ADRs 0002–0004 in M1.
  Remaining open question: whether executors own transport sessions or workers
  hand them handles (see `context.md`). This should be settled in M2.

## Just Finished

**Milestone 1 — Worker Contract.** Implemented `Task`, `Response`/`ResponseStatus`,
`BaseExecutor`, and `BaseWorker` with full type hints, async lifecycle,
error taxonomies, and Template Method `send()`. 42 unit tests, 99% coverage,
all passing. ADRs 0002–0004 record the three contract decisions. See `changelog.md`
entry `[0.2.0]` and `progress.md` M1 retrospective.

---

## How to update this file

- When a task starts: move it from "Next Action" to "Active Task".
- When a task finishes: move it to "Just Finished" (keep only the latest), update
  `progress.md`, and write the next proposed action.
- Keep this file short. Detail lives in `context.md`, `architecture.md`, and ADRs.
