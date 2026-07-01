# Architecture

> The structural design contract of CouncilOS. This is **load-bearing**: an
> implementer must not contradict it without an approved ADR superseding the part
> in question. Humans read this; AI agents are bound by it.

---

## 1. Intent

CouncilOS sends a prompt to several frontier LLMs and reconciles their answers into
one trustworthy verdict. The architecture exists to make that **vendor-independent,
observable, and reliable**.

The guiding principle is **separation by role**:

```
Executors execute.  Workers communicate.  Protocols coordinate.  Core orchestrates.
```

---

## 2. Layered Architecture

```
                        ┌─────────────────────────────────────┐
                        │                 CORE                 │
                        │   orchestrates the entire council   │
                        │  fan-out · retry · collect · judge  │
                        └─────────────────────────────────────┘
            ▲                    ▲                     ▲
            │                    │                     │
   ┌────────────────┐  ┌──────────────────┐  ┌──────────────────┐
   │   PROTOCOLS    │  │     WORKERS      │  │    EXECUTORS     │
   │  coordinate    │  │   communicate    │  │    execute       │
   │  interactions  │  │   with ONE model │  │  ONE atomic act  │
   │  between       │  │   (lifecycle:    │  │  (HTTP request,  │
   │  workers       │  │   start/send/    │  │   browser prompt │
   │                │  │   stop)          │  │   + read)        │
   └────────────────┘  └──────────────────┘  └──────────────────┘
                                                     │
                                                     ▼
                                     ┌───────────────────────────┐
                                     │  TRANSPORT (invisible to  │
                                     │  Core/Protocols/Workers): │
                                     │   REST APIs · Playwright  │
                                     │   browser sessions        │
                                     └───────────────────────────┘
```

### Dependency direction

```
core  ──▶  protocols  ──▶  workers  ──▶  executors  ──▶  transport
```

A layer may depend on the layer below it and on shared types in `app/core/types`.
A layer **never** depends upward. The core never imports a concrete worker by name
except at a single registration point (the future Worker Registry, Milestone 6).

---

## 3. Layer responsibilities

### Executors (`app/executors/`)
- Perform **one atomic action** and return a raw result.
- Examples: `http_post_executor`, `browser_prompt_executor`.
- Stateless with respect to council logic. They do not know about retries,
  judging, or other workers.
- Two families are anticipated: **API executors** (HTTP/SDK) and **browser
  executors** (Playwright DOM). They share a common `Executor` contract.

### Workers (`app/workers/`)
- Own the **full lifecycle** of one external model: `start → send(prompt) → stop`.
- Use one or more executors under the hood.
- Return a **normalized `WorkerResponse`** (schema TBD — see open questions).
- Hide all model-specific quirks (selectors, SDK shapes, auth refresh) inside.
- One worker per model: `ChatGPTWorker`, `GeminiWorker`, `PerplexityWorker`.
- **Never** call another worker. Coordination is the protocol layer's job.

### Protocols (`app/protocols/`)
- Coordinate **how a set of workers interact**: round-robin, parallel fan-out,
  debate, voting.
- Operate purely against the abstract `Worker` interface; they are vendor-blind.
- Do not perform I/O themselves — they ask workers to.

### Core (`app/core/`)
- The orchestrator: composes protocols + workers + the retry engine + the response
  collector + the judge into an end-to-end run.
- Holds the public entry point of the framework.
- Owns cross-cutting types in `app/core/types.py` (shared by all layers).

---

## 4. Supporting modules

| Module            | Responsibility                                      |
|-------------------|-----------------------------------------------------|
| `app/storage/`    | Persistence: run transcripts, episodic memory.      |
| `app/utils/`      | Shared infra: logging, timing, config helpers.      |
| `app/config/`     | Settings, env loading, worker configuration.        |
| `app/cli/`        | Command-line entry points (thin; delegates to core).|

These support the four layers; they are not themselves layers.

---

## 5. The end-to-end flow (target state, post-Milestone 9)

```
User prompt
   │
   ▼
Core: select council (Worker Registry) ──────────────────────┐
   │                                                          │
   ▼                                                          │
Protocol: fan-out ──┬──▶ Worker: ChatGPT  ──▶ Executor ──▶ ChatGPT
                   ├──▶ Worker: Gemini   ──▶ Executor ──▶ Gemini
                   └──▶ Worker: Perplex ──▶ Executor ──▶ Perplexity
                                  │
                  (Retry Engine wraps each worker call)
                                  │
                                  ▼
                   Response Collector: normalize + gather
                                  │
                                  ▼
                            Judge: synthesize
                                  │
                                  ▼
                   Final verdict + provenance trail
```

Each box maps to a frozen milestone (see `roadmap.md`).

---

## 6. Cross-cutting contracts

- **Shared types** live in `app/core/types.py`. Every layer imports from here;
  no layer defines a type that another layer must accept.
- **Errors** form a typed hierarchy rooted at `WorkerError` (workers) and an
  analogous `ExecutorError`. Retries branch on retryable-vs-terminal.
- **Observability** flows through the shared logger (`app/utils/`). Every layer
  logs at its own boundaries; nothing reaches down to `print`.

---

## 7. What is explicitly NOT here yet

The architecture above is the **target**. As of Milestone 0, none of the layers
contain code — only package skeletons. The milestones build this out one contract
at a time:

- **M1** defines the `Worker` contract (and shared types).
- **M2** defines the `Executor` contract.
- **M3–M5** fill in concrete workers.
- **M6–M9** add registry, retry, collection, judging.

Do not build ahead of the milestone sequence. See `roadmap.md`.

---

## 8. Changing this document

This is a contract. Any change to the layering, dependency direction, or
responsibilities requires an ADR in `planning/decisions/` and explicit approval.
