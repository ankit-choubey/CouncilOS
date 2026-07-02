# ADR-0002: Response schema is a typed object, not a bare string

- **Status**: Accepted
- **Date**: 2026-07-02

## Context
Workers must return something to the caller. The simplest option is a bare `str`.
But Milestone 8 (Response Collector) and Milestone 9 (Judge) need to know *which*
worker produced an answer, how long it took, and whether it succeeded or failed.
A bare string carries none of that.

## Decision
`Response` is a frozen dataclass with typed fields:
`text`, `worker_name`, `status` (enum), `latency_ms`, `created_at`, `error`.
A `ResponseStatus` enum (`SUCCESS` / `FAILED`, inheriting `str` for JSON
serializability) classifies outcomes.

A success with empty text is a validation error (fail loud). A failure with no
error message auto-fills `"Unknown error"` (never silently None).

## Consequences
- **Positive:** Provenance, latency, and status are first-class on every response.
  The collector and judge have structured data to work with.
- **Negative:** Slightly more ceremony than `return "answer"`. Workers construct a
  Response object — but `BaseWorker.send()` builds it automatically (Template
  Method), so concrete workers just return a string from `_send`.
- **Neutral:** Frozen + slots makes Response immutable and cheap, safe to share
  across concurrent fan-out.

## Alternatives considered
- **Bare `str`.** Rejected: no provenance or latency; every consumer would have to
  track metadata out-of-band.
- **`dict[str, Any]`.** Rejected: no type safety, easy to miss keys, `Any` is a
  code smell per CODING_STANDARDS.
- **Pydantic model.** Rejected for now (adds a heavy dependency for four fields);
  can revisit if validation becomes complex post-M9.
