# Roadmap (Frozen)

> The milestone sequence is **frozen**. It will not be reordered. Scope inside a
> milestone may flex, but the sequence and what each milestone delivers are fixed.
> Change requests to the sequence require an ADR and explicit approval.

---

## Through Milestone 9 = usable CouncilOS core

| #  | Milestone            | Delivers                                                            |
|----|----------------------|---------------------------------------------------------------------|
| 0  | Repository foundation| `.ai/` + `planning/` split, layered contract, package skeleton      |
| 1  | Worker Contract      | The `Worker` interface + shared types every model implements         |
| 2  | Executor Contract    | The `Executor` interface (HTTP + browser families)                   |
| 3  | ChatGPT Worker       | First concrete worker (browser-executor backed)                      |
| 4  | Gemini Worker        | Second worker, proving the contract generalizes                     |
| 5  | Perplexity Worker    | Third worker, cementing the pattern                                 |
| 6  | Worker Registry      | Discover/select workers at runtime; the council can be assembled    |
| 7  | Retry Engine         | Transparent retry of flaky workers, retryable-vs-terminal aware     |
| 8  | Response Collector   | Gather + normalize every worker's response                           |
| 9  | Judge (Simple)       | Synthesize a single verdict from collected responses                 |

**At the end of Milestone 9, CouncilOS is a usable system.** A prompt goes in,
multiple models answer, a judge returns one reconciled verdict with provenance.

Everything after Milestone 9 is enhancement: richer protocols (debate, voting),
episodic memory, RAG, a dashboard, red-teaming, production packaging. Those will
be planned when the core exists.

---

## Sequencing rationale

The contracts come first because every layer depends on them:

- You cannot build a worker without the **Worker contract** (M1).
- You cannot build a concrete worker without the **Executor contract** (M2).
- You cannot prove the contract generalizes with only one worker (M3→M4→M5).
- You cannot fan out without a **Registry** to know who exists (M6).
- Fan-out is useless without **Retry** (M7) and **Collection** (M8).
- Collection is useless without a **Judge** to reconcile it (M9).

Skipping ahead breaks the dependency chain. Don't.

---

## Out of scope (for now)

These are real future work but are explicitly **not** in the frozen core:

- A GUI / real-time dashboard.
- Long-term episodic vector memory.
- RAG / retrieval pipelines.
- Benchmark suites (MMLU, GSM8K).
- Docker packaging, FastAPI service, deployment.

They will be planned as their own milestones after M9.
