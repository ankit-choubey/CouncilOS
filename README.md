# CouncilOS

> A multi-model orchestration framework. Send one prompt to several frontier LLMs,
> reconcile their answers through a judge, get one trustworthy verdict.

A single model is a guess. **A council of independent models is a decision.**
CouncilOS fans a query out across heterogeneous backends (ChatGPT, Gemini,
Perplexity, …) and synthesizes a single, explainable answer with a full provenance
trail — without taking a hard dependency on any one vendor.

---

## Status

**Milestone 0 — Repository foundation** is complete. The contracts, structure, and
documentation system are in place. The first production code (the Worker Contract,
Milestone 1) is next. See `planning/roadmap.md` for the frozen milestone sequence.

---

## Understand the project in 10 minutes

This repository is built to be understood from the files alone — no chat history
required.

- **For AI coding agents:** read `.ai/AGENT.md` first. It tells you what to read
  and how to operate.
- **For humans:** start at `planning/current_focus.md`, then `planning/architecture.md`
  and `planning/roadmap.md`.

---

## Repository layout (two doc audiences)

```
.ai/         # AI-readable: contracts, rules, standards, prompts
planning/    # Human-readable: focus, architecture, roadmap, decisions, changelog
app/         # The framework (core, workers, executors, protocols, storage, utils, config, cli)
tests/       # unit / integration / browser / fixtures
scripts/     # setup.sh, run.sh, test.sh, format.sh
```

The layered contract (see `planning/architecture.md`):

```
Executors execute.  Workers communicate.  Protocols coordinate.  Core orchestrates.
```

---

## Quick start

```bash
# 1. Create an isolated virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Upgrade pip, then install the project + dev tooling
python -m pip install --upgrade pip
pip install -e ".[dev]"

# 3. Configure environment
cp .env.example .env        # then edit .env with your keys

# 4. Run the test suite
./scripts/test.sh
```

Or, all-in-one:

```bash
./scripts/setup.sh
```

---

## Tooling

- **Python 3.10+**, modern `pyproject.toml` (no `setup.py` / `requirements.txt`).
- **black** + **isort** (formatting), **ruff** (lint), **mypy --strict** (types).
- **pytest** + **pytest-asyncio** + **pytest-cov** (tests).
- `./scripts/format.sh` → format + lint
- `./scripts/test.sh` → unit suite + coverage

---

## Engineering laws (the short version)

1. Architecture before implementation.
2. One feature per commit. One responsibility per module.
3. Every new feature requires tests.
4. Update `planning/` after implementation — the repo is the source of truth.
5. Never hardcode model-specific behavior outside workers.
6. Respect the layered contract.

Full version: `.ai/DEVELOPMENT_RULES.md`.

---

## License

MIT — see `LICENSE` (to be added).
