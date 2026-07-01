# Working Context

> Short-term, session-scoped notes: decisions made in conversation, half-formed
> thoughts, pointers to "where we left off". This is the scratchpad. It is *not*
> a contract — anything load-bearing graduates into `architecture.md` or an ADR.

---

## State right now

- Repository restructured to the `.ai/` + `planning/` split (2026-07-01).
- Old debate-era code (`app/agents`, `app/automation`, advocate/critic/judge)
  removed. It lives in git history under the pre-restructure commits if ever
  needed. **It is superseded** by the worker/executor/protocol/core layering.
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

1. Response schema for `WorkerResponse` — bare string vs typed object.
2. Async vs sync worker interface.
3. Failure taxonomy (retryable vs terminal).
4. Whether executors own sessions or workers hand them handles.
5. Judge input shape.

These are mirrored in `.ai/PROJECT_CONTEXT.md → Open Design Questions` and must be
closed with ADRs before the relevant milestone's code lands.

## Scratch

- (empty)
