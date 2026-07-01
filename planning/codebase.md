# Codebase Map

> A live map of every module and its single-sentence responsibility.
> An AI agent reads this to orient without grepping. **Update it whenever a module
> is added, removed, or repurposed** — a stale map defeats its purpose.

Legend: ✅ implemented · 🔲 placeholder/skeleton · 📁 directory only

---

## Repository layout

```
CouncilOS/
├── .ai/                  # AI-readable contracts & prompts (agents read this)
│   ├── AGENT.md
│   ├── DEVELOPMENT_RULES.md
│   ├── CODING_STANDARDS.md
│   ├── PROJECT_CONTEXT.md
│   └── PROMPTS/           # bootstrap, implementation, review, debug
│
├── planning/             # Human-readable project state
│   ├── current_focus.md   # what's happening right now
│   ├── context.md         # session scratchpad
│   ├── architecture.md    # the structural contract
│   ├── codebase.md        # THIS FILE
│   ├── progress.md        # milestone & task status
│   ├── roadmap.md         # frozen milestone sequence
│   ├── testing.md         # testing contract
│   ├── changelog.md       # what changed and why
│   ├── research_notes.md  # hard-won findings, preserved
│   ├── decisions/         # ADRs
│   └── session_logs/      # per-session run logs (gitignored)
│
├── app/                  # The framework (Python package)
│   ├── core/             # orchestration + shared types
│   ├── workers/          # one Worker per external model
│   ├── executors/        # one atomic action per executor
│   ├── protocols/        # how workers interact
│   ├── storage/          # persistence & memory
│   ├── utils/            # logging, timing, helpers
│   ├── config/           # settings & env
│   └── cli/              # thin command-line entry points
│
├── tests/                # mirrors app/
│   ├── unit/
│   ├── integration/      # opt-in; may hit real services
│   ├── browser/          # opt-in; drives real browsers
│   └── fixtures/
│
├── scripts/              # setup.sh, run.sh, test.sh, format.sh
├── configs/              # run configurations (committed)
├── docs/                 # human-facing docs beyond planning/
├── logs/                 # runtime logs (gitignored)
├── runs/                 # run artifacts/transcripts (gitignored)
│
├── pyproject.toml        # build & dependency config (modern; no setup.py)
├── .env.example          # template; copy to .env (gitignored)
├── .gitignore
└── README.md
```

---

## Module status

### `app/` — the framework

| Path                       | Status | Responsibility                                          |
|----------------------------|--------|---------------------------------------------------------|
| `app/__init__.py`          | 🔲     | Package marker.                                         |
| `app/core/`                | 🔲     | Orchestrates the council end-to-end.                    |
| `app/core/types.py`        | 🔲     | Shared types used across all layers (M1).               |
| `app/workers/`             | 🔲     | One Worker per external model. **Next: the contract.**  |
| `app/workers/base.py`      | 🔲     | Abstract `Worker` + `BaseWorker` (Milestone 1).         |
| `app/executors/`           | 🔲     | Atomic actions (HTTP / browser). Contract in M2.        |
| `app/protocols/`           | 🔲     | Coordinate worker interactions.                         |
| `app/storage/`             | 🔲     | Persistence: transcripts, episodic memory.              |
| `app/utils/`               | 🔲     | Shared logger, timing, helpers.                         |
| `app/utils/logger.py`      | 🔲     | Rich-backed shared console logger.                      |
| `app/config/`              | 🔲     | Settings + env loading.                                 |
| `app/cli/`                 | 🔲     | Thin CLI delegating to core.                            |

### `tests/`

| Path                  | Status | Responsibility                                   |
|-----------------------|--------|--------------------------------------------------|
| `tests/unit/`         | 🔲     | Fast, no-network unit tests (mirror `app/`).     |
| `tests/integration/`  | 🔲     | Opt-in tests that may hit real APIs.             |
| `tests/browser/`      | 🔲     | Opt-in tests that drive real browsers.           |
| `tests/fixtures/`     | 🔲     | Shared fixtures / sample data.                   |

### `scripts/`

| Path              | Status | Responsibility                                  |
|-------------------|--------|-------------------------------------------------|
| `scripts/setup.sh`| 🔲     | Create venv, install deps, ready in minutes.    |
| `scripts/run.sh`  | 🔲     | Run the core entry point.                       |
| `scripts/test.sh` | 🔲     | Run the test suite.                             |
| `scripts/format.sh`| 🔲    | Run black + isort + ruff.                       |

---

## Update protocol

When you add, remove, or change the responsibility of a module:

1. Update its row here (status 🔲→✅ and the one-sentence responsibility).
2. If it changes the layering, update `architecture.md` and write an ADR.
3. Mention it in `changelog.md` under the relevant version.

A module that is not listed here does not exist as far as the contract is concerned.
