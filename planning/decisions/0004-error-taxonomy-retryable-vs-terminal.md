# ADR-0004: Error taxonomy — retryable vs terminal, per layer

- **Status**: Accepted
- **Date**: 2026-07-02

## Context
The Retry Engine (Milestone 7) needs to know whether a failure is worth retrying.
If every failure is an opaque exception, the retry engine must guess — fragile and
wrong. The classification must happen at the layer that understands the failure,
not at a downstream engine that has no context.

## Decision
Each layer (executor, worker) has a typed exception hierarchy:

```
ExecutorError / WorkerError  (base)
├── RetryableXxxError        (transient: network, rate limit, DOM lag)
└── TerminalXxxError         (permanent: auth, malformed request, 4xx)
```

`BaseWorker.send()` catches `WorkerError` and wraps it into a `FAILED` Response
(so the collector always gets a Response, never an exception). Unexpected
(non-WorkerError) exceptions are **not** caught — they are bugs, and per the coding
standards we fail loud.

**Tradeoff noted:** Because `send()` converts `WorkerError` → FAILED Response,
the Retry Engine (M7) has two paths: inspect the Response status, or call the
lower-level `_send` that raises. This bridge is intentionally deferred (rule of
three) — it will be designed when the Retry Engine exists and the actual usage
pattern is known.

## Consequences
- **Positive:** The Retry Engine will branch cleanly on `isinstance(exc, RetryableXxxError)`.
  No guessing, no magic strings, no heuristics.
- **Negative:** Concrete workers must choose the right error subclass. A mis-
  classified error (e.g. wrapping a 403 as RetryableWorkerError) would cause
  wasted retries. Mitigated by clear docstrings and examples.
- **Neutral:** The hierarchy is small (3 classes per layer). It doesn't grow
  until a real need justifies it.

## Alternatives considered
- **Single exception type with a `.retryable` flag.** Rejected: less discoverable,
  no IDE/type-checker support, easier to forget the flag.
- **Error codes (int/str enum).** Rejected: requires importing a code registry,
  adds indirection, exceptions with meaningful class names are more Pythonic.
- **Let the Retry Engine classify.** Rejected: the retry engine has no transport-
  level context. A 429 and a 401 look identical at that layer.
