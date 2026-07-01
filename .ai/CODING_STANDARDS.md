# CODING_STANDARDS.md — How Code is Written in CouncilOS

> Enforced by convention and review. A reviewer (human or AI) may reject code that
> violates these without further justification.

---

## Language & tooling

- **Python 3.10+** (use modern syntax: `match`, `|` union types, `dataclasses`).
- **Dependency & build config:** modern `pyproject.toml`. **No** `requirements.txt`
  or `setup.py`.
- **Formatting:** `black` (line length 88).
- **Import sorting:** `isort` (profile `black`).
- **Linting:** `ruff`.
- **Type checking:** `mypy --strict` on `app/`. Types are mandatory, not decorative.
- **Testing:** `pytest`. Async tests use `pytest-asyncio`.
- **Run the suite:** `./scripts/test.sh`. Don't assume tests pass — run them.

---

## Structure

- **Module size:** keep files under **~300 lines** where practical. Split when they
  grow. A 600-line file is a smell.
- **One responsibility per module** (see `DEVELOPMENT_RULES.md` rule 3).
- **Public API at the top**, private helpers below, separated by a comment banner.
- **No `from x import *`.** Ever.
- **Group imports:** stdlib → third-party → local, with blank lines between.

```python
from __future__ import annotations

import asyncio
from dataclasses import dataclass

from rich.console import Console

from app.core.types import WorkerResponse
```

---

## Naming

| Element      | Convention        | Example            |
|--------------|-------------------|--------------------|
| Module/file  | `snake_case`      | `worker_base.py`   |
| Class        | `PascalCase`      | `ChatGPTWorker`    |
| Function     | `snake_case`      | `send_prompt`      |
| Constant     | `UPPER_SNAKE`     | `DEFAULT_TIMEOUT`  |
| Type alias   | `PascalCase`      | `PromptText`       |
| Private      | leading `_`       | `_stabilize_text`  |

Names are ** pronounceable and intention-revealing.** `d`, `tmp`, `x2` are not
acceptable outside a tight loop or comprehension.

---

## Typing

- **Annotate every public function** (parameters and return type).
- Use `from __future__ import annotations` so annotations are strings.
- Prefer `dataclass` / `pydantic` models over loose dicts for structured data.
- Use `Protocol` for contracts the system depends on (e.g. `Worker`).
- `Any` is a code smell. If you reach for it, reconsider the types above you.

```python
from typing import Protocol

class Worker(Protocol):
    async def send(self, prompt: str) -> WorkerResponse: ...
```

---

## Error handling

- **Define a typed exception hierarchy** per layer, e.g.
  `WorkerError → RetryableWorkerError / TerminalWorkerError`.
- **Never bare `except:`.** Catch the specific exception, or let it propagate.
- **Distinguish retryable from terminal failures.** Network blip = retryable;
  auth rejected = terminal. The Retry Engine depends on this.
- **Fail loudly in development.** Don't swallow exceptions into silent `None`s.

---

## Async

- **Workers are async.** Fan-out concurrency is core to the vision, so design for
  it from Milestone 1. `async def send(...)` not `def send(...)`.
- **No blocking calls inside async code.** No `time.sleep`, no `requests`. Use
  `asyncio.sleep` and async HTTP.
- **Cancellation must be clean.** Propagate `CancelledError`; release resources.

---

## Logging & observability

- Use the shared logger from `app/utils/` (rich-backed console). Don't `print`.
- Log at boundaries: prompt sent, response stabilized, worker retried, verdict.
- Never log secrets, full prompt contents, or PII at INFO.

---

## Tests

- **Layout mirrors `app/`.** A module `app/workers/chatgpt.py` is tested by
  `tests/unit/workers/test_chatgpt.py`.
- **One test class/function per behavior.** Name tests by behavior, not by method:
  `test_returns_stabilized_response_when_stream_settles`.
- **Fixtures** live in `tests/fixtures/` and `conftest.py`.
- **No network in unit tests.** Mock executors / HTTP. Browser and live-API tests
  live in `tests/browser/` and `tests/integration/` and are opt-in.
- **Every public function and every contract has at least one test.**

---

## Comments & docstrings

- **Docstring every public module, class, and function.** Triple-quoted, imperative
  summary first line.
- Comments explain **why**, not **what**. If the code needs a `# what it does`
  comment, the code is unclear — fix the code.
- Delete commented-out code. Git remembers it.

---

## File header

Every Python module starts with a one-line module docstring:

```python
"""Abstract Worker contract implemented by every concrete worker."""
```

---

## When standards conflict

Readability beats cleverness.
Explicit beats implicit.
Concrete beats abstract (until the rule of three triggers).
A passing test suite beats all of the above.
