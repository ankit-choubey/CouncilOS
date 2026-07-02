# Architecture Decision Records (ADR) — Index

> ADRs record *why* a decision was made, so the future doesn't relitigate it.
> Numbered, one file each, newest at the bottom. An ADR is never deleted; it is
> marked **Superseded** with a pointer to its replacement.

## ADR template

```markdown
# ADR-XXX: [Title]

- **Status**: Draft | Proposed | Accepted | Superseded | Deprecated
- **Date**: YYYY-MM-DD

## Context
(What is the problem? What are the constraints and forces?)

## Decision
(What did we decide? State it unambiguously.)

## Consequences
- Positive: …
- Negative: …
- Neutral: …

## Alternatives considered
(What else was on the table, and why not?)
```

## Register

| ADR  | Title                                                | Status   | Date       |
|------|------------------------------------------------------|----------|------------|
| 0001 | Repository foundation & the layered contract         | Accepted | 2026-07-01 |
| 0002 | Response schema is a typed object, not a bare string | Accepted | 2026-07-02 |
| 0003 | Async-first contract from day one                    | Accepted | 2026-07-02 |
| 0004 | Error taxonomy — retryable vs terminal, per layer    | Accepted | 2026-07-02 |

---

## How to add an ADR

1. Copy the template into `0NNN-short-title.md` (next number, zero-padded).
2. Fill every section. "Alternatives considered" is mandatory, not optional.
3. Add a row to the register above.
4. Reference it from `changelog.md` and, where relevant, `architecture.md`.

An ADR exists so that when someone (human or AI) wants to change the decision later,
they can read the original reasoning and decide on the merits.
