# PROJECT_CONTEXT.md — Executive Summary for AI Agents

> Paste-grade context. Any AI assistant reading this should understand **what
> CouncilOS is**, **why it exists**, and **where it is** within five minutes.

---

## What is CouncilOS?

CouncilOS is a **multi-model orchestration framework**. It sends the same prompt
(or a coordinated family of prompts) to several frontier LLMs — ChatGPT, Gemini,
Perplexity, and others — and synthesizes a single, high-quality answer through a
judge.

The core insight: **a single model is a guess; a council of independent models is
a decision.** By fanning a query out across heterogeneous backends and reconciling
their outputs, CouncilOS reduces hallucination, surfaces disagreement, and produces
more trustworthy answers than any one model alone.

---

## Why does it exist?

1. **Model independence.** No single vendor is a dependency. Workers abstract each
   model behind a uniform contract.
2. **Quality through diversity.** Different models fail differently; a judge that
   reconciles them beats relying on any one.
3. **Cost control.** Free / web-tier access (browser automation) and paid API tiers
   are interchangeable behind the same worker interface.
4. **Auditability.** Every model's raw contribution is preserved, so the final
   answer is explainable, not a black box.

---

## Current Architecture (Layered Contract)

```
┌──────────────────────────────────────────────────────────┐
│                        CORE                              │
│            orchestrates the whole council                │
│   (fan-out, retry, collection, judging, fan-in)          │
└──────────────────────────────────────────────────────────┘
        ▲                ▲                 ▲
        │                │                 │
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  PROTOCOLS    │ │   WORKERS     │ │   EXECUTORS   │
│ coordinate    │ │ communicate   │ │ execute a     │
│ how workers   │ │ with one      │ │ single action │
│ interact      │ │ external model│ │ (API/DOM call)│
└───────────────┘ └───────────────┘ └───────────────┘
```

One sentence per layer:

- **Executors** execute one atomic action (an HTTP call, a browser prompt+read).
- **Workers** own the lifecycle of one external model: send, stream, stabilize,
  return a normalized response. They use executors; they never orchestrate peers.
- **Protocols** coordinate how workers interact (round-robin, debate, voting).
- **Core** orchestrates the whole council end to end.

This is a **contract**, not a suggestion. See `planning/architecture.md`.

---

## Long-Term Vision

A system where an operator asks one question and, behind the scenes, CouncilOS:

1. Selects a council of complementary models (Worker Registry).
2. Fans the prompt out to all of them concurrently.
3. Retries flaky workers transparently (Retry Engine).
4. Collects every normalized response (Response Collector).
5. Judges and synthesizes a single answer (Judge).
6. Returns the verdict with a full provenance trail.

The end state is a reliable, vendor-independent reasoning engine.

---

## Current Milestone

**Milestone 1 — Worker Contract.**

The repository foundation (Milestone 0) is complete. The next piece of production
code is the abstract `Worker` contract and its supporting data types — the single
interface every concrete worker (ChatGPT, Gemini, Perplexity…) will implement.
Nothing else can be built until this contract exists.

See `planning/current_focus.md` for the precise active task.

---

## Future Roadmap (frozen)

| #  | Milestone            | Status      |
|----|----------------------|-------------|
| 0  | Repository foundation| ✅ Done     |
| 1  | Worker Contract      | 🔜 Next     |
| 2  | Executor Contract    | Pending     |
| 3  | ChatGPT Worker       | Pending     |
| 4  | Gemini Worker        | Pending     |
| 5  | Perplexity Worker    | Pending     |
| 6  | Worker Registry      | Pending     |
| 7  | Retry Engine         | Pending     |
| 8  | Response Collector   | Pending     |
| 9  | Judge (Simple)       | Pending     |

Everything through Milestone 9 is the **usable core**. Beyond that is enhancement.

---

## Important Constraints

- **Python 3.10+**, modern `pyproject.toml` (no `requirements.txt` / `setup.py`).
- **No model-specific behavior leaks out of workers.** The core, protocols, and
  executors must remain vendor-agnostic. Hardcoding ChatGPT quirks in core is a bug.
- **Browser-automation workers and API workers share the same `Worker` contract.**
  The transport is invisible to the caller.
- **Every public function and contract needs tests** before it is considered done.
- **The layered boundaries are load-bearing.** Do not collapse them for speed.
- **No code without an approved plan** (see `AGENT.md` startup sequence).

---

## Open Design Questions

These are unresolved and should *not* be silently decided by an implementer:

1. **Response schema.** What exactly does a Worker return? A bare string? A typed
   `WorkerResponse` with tokens/latency/provenance? *(To be settled in M1.)*
2. **Sync vs async.** Do workers expose an async interface from day one (concurrent
   fan-out is core to the vision), or start synchronous and add async later?
3. **Failure model.** What does a worker return/raise on timeout, DOM change, or
   auth failure? How does the Retry Engine distinguish retryable from terminal?
4. **Transport of executors.** Does the Executor contract own the browser/HTTP
   session, or does the Worker own it and hand the executor a handle?
5. **Judge input.** Does the Judge consume raw strings, normalized responses, or a
   structured transcript? This ripples back into the response schema.

Decisions on these are recorded in `planning/decisions/` as ADRs when made.
