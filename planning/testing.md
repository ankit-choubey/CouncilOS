# Testing Contract

> How we test CouncilOS. This is binding: a feature without a test is unfinished.

---

## Principles

1. **Tests describe behavior, not implementation.** Name them for the behavior:
   `test_returns_stabilized_response_when_stream_settles`, not `test_send_1`.
2. **Unit tests are fast and network-free.** They mock executors and HTTP.
3. **Live tests are opt-in.** Real API and browser tests never run in the default
   suite — they cost money, need credentials, and are flaky.
4. **Every public function and every contract has at least one test.**
5. **Bugs are reproduced by a failing test first**, then fixed.

---

## Layout

`tests/` mirrors `app/`:

```
tests/
├── unit/             # fast, hermetic — run by default
│   ├── core/
│   ├── workers/      # e.g. test_worker_contract.py
│   ├── executors/
│   └── protocols/
├── integration/      # opt-in; may hit real APIs (needs -m integration)
├── browser/          # opt-in; drives real browsers (needs -m browser)
├── fixtures/         # shared sample data
└── conftest.py       # shared fixtures
```

A module `app/workers/base.py` is tested at `tests/unit/workers/test_base.py`.

---

## Tooling

- **Runner:** `pytest`.
- **Async:** `pytest-asyncio` (`asyncio_mode = auto` in config).
- **Coverage:** `pytest-cov`, target ≥ 85% on `app/`, reported on every run.
- **Mocks:** `pytest`'s monkeypatch / `unittest.mock` for executors and HTTP.

---

## Markers

| Marker       | When it runs                          | Example use                       |
|--------------|---------------------------------------|-----------------------------------|
| *(none)*     | Default — always                      | Unit tests                        |
| `integration`| Only with `-m integration`            | Real API calls (cost tokens)      |
| `browser`    | Only with `-m browser`                | Playwright against live ChatGPT   |

`scripts/test.sh` runs **only** the default (unmarked) suite. CI runs the same.
Integration/browser tests are a manual, deliberate choice.

---

## What to test, per layer

- **Contracts (`Worker`, `Executor`):** test via a `FakeWorker` / `FakeExecutor`
  that implements the protocol. Verify the lifecycle, return shape, and that errors
  classify as retryable or terminal.
- **Concrete workers:** test against fakes for the executor; the *real* model call
  is an opt-in browser/integration test.
- **Protocols:** test against fake workers that scripts return canned responses.
- **Core:** test against fake protocols/workers; assert the end-to-end shape.

---

## Running

```bash
./scripts/test.sh                 # default unit suite (+ coverage)
pytest -m integration             # opt-in real API tests
pytest -m browser                 # opt-in browser tests
```

If a test is failing, **fix it or revert**. Never delete, skip, or broaden an
exception to make it green. (See `.ai/DEVELOPMENT_RULES.md`.)
