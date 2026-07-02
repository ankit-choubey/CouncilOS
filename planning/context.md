# Working Context

> Short-term, session-scoped notes: decisions made in conversation, half-formed
> thoughts, pointers to "where we left off". This is the scratchpad. It is *not*
> a contract — anything load-bearing graduates into `architecture.md` or an ADR.

---

## State right now

- Milestone 1 complete (2026-07-02). All four core contracts implemented + tested.
- The system `python3` is 3.9.6; project requires 3.10+. The `.venv` is built with
  `/usr/local/bin/python3.14`. Document this in setup.sh notes if it trips anyone.
- One valuable artifact was preserved as research: the browser-automation findings
  (persistent profiles, anti-detection, DOM stream-stabilization). See
  `research_notes.md` — they will feed Milestone 3 (ChatGPT Worker) directly.

## Conventions agreed in conversation

- **No `requirements.txt` / `setup.py`.** Use modern `pyproject.toml`.
- **Tooling:** black, isort, ruff, mypy --strict, pytest + pytest-asyncio.
- **Virtualenv folder is `.venv`** (not `venv`).
- **Every session starts with the bootstrap prompt** (`.ai/PROMPTS/bootstrap.md`).
  The agent reads state, never remembers it.

## Open threads (to resolve soon)

1. Response schema for `WorkerResponse` — bare string vs typed object. **→ Closed:
   ADR-0002. Typed `Response` dataclass.**
2. Async vs sync worker interface. **→ Closed: ADR-0003. Async-first.**
3. Failure taxonomy (retryable vs terminal). **→ Closed: ADR-0004. Typed error
   hierarchy per layer.**
4. Whether executors own sessions or workers hand them handles. **→ Still open.
   To be settled in M2 when concrete executor families are designed.**
5. Judge input shape. **→ Still open. To be settled in M9.**

Remaining open questions are mirrored in `.ai/PROJECT_CONTEXT.md → Open Design
Questions` and must be closed with ADRs before the relevant milestone's code lands.

## Scratch

- (empty)
