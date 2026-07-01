# ADR-0001: Repository foundation & the layered contract

- **Status**: Accepted
- **Date**: 2026-07-01

## Context

CouncilOS began as an early prototype organized around an *advocate/critic/judge
debate* with a Playwright-driven ChatGPT client (`app/automation`). That code
embodied two problems:

1. **Architecture was implicit.** The relationships between agents, the browser
   driver, the parser, and the judge lived in conversation memory, not in the repo.
   Onboarding a new AI session meant re-explaining the whole project.
2. **Boundaries were blurred.** Orchestration, DOM detail, and evaluation logic
   were tangled. Scaling to a second or third model would have meant copy-paste,
   not abstraction.

We need a foundation where (a) any AI agent or human can understand the project
from the repository alone in under 10 minutes, and (b) adding a new model is a
matter of implementing a contract, not rewriting orchestration.

## Decision

1. **Split documentation by audience.**
   - `.ai/` holds AI-readable contracts, rules, standards, and prompts.
   - `planning/` holds human-readable project state (focus, architecture, progress,
     roadmap, decisions, changelog).
   - The repository is the source of truth. Agents **read state**, they do not
     **remember** it.

2. **Adopt a strict four-layer contract** as the system's structural law:

   ```
   Executors execute.  Workers communicate.  Protocols coordinate.  Core orchestrates.
   ```

   - **Executors** perform one atomic action (HTTP call, browser prompt+read).
   - **Workers** own the lifecycle of one external model and return a normalized
     response; they never orchestrate peers.
   - **Protocols** coordinate how workers interact; they are vendor-blind.
   - **Core** orchestrates the whole council end to end.

   Dependencies flow only downward:
   `core → protocols → workers → executors → transport`. No upward imports except
   at the future registry registration point.

3. **Freeze a milestone sequence (M0–M9)** that builds the contracts before the
   concrete parts, ending in a usable core (see `roadmap.md`).

4. **Remove the old prototype code.** It is superseded by the layering. Hard-won
   browser-automation findings are preserved in `research_notes.md` to feed M3.

## Consequences

- **Positive:**
  - A new model is a new Worker — it cannot corrupt the core or protocols.
  - Onboarding is documentation-driven; switching AI providers (Claude/GPT/Gemini)
    is a non-event because context lives in the repo.
  - The 10-minute comprehensibility bar is enforceable and testable.
- **Negative:**
  - More upfront structure and ceremony than a prototype needs; small tasks carry
    doc-update overhead.
  - The contract constrains "quick" solutions that would cross layers — this is
    intentional but can feel slow.
- **Neutral:**
  - Browser-automation workers and API workers now share one interface; the
    transport difference is hidden inside executors.

## Alternatives considered

- **Keep the debate-era layout and refactor in place.** Rejected: the boundaries
  were too entangled, and implicit architecture is the root problem we are fixing.
- **A flatter "agents + tools" design** (no executor/protocol split). Rejected: it
  does not separate "talk to one model" from "coordinate many models", which is the
  exact distinction we need to scale the council.
- **Documentation in a single `/docs`.** Rejected: it conflates human and AI
  readers. The `.ai/` vs `planning/` split makes the audience explicit and keeps
  AI contracts machine-stable.
