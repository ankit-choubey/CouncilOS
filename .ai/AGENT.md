# AGENT.md — The AI Implementation Engineer's Charter

> This file is the **entry point** for any AI coding assistant joining CouncilOS.
> It defines *how* an agent must operate on this repository.
> It is AI-readable, not human documentation. Humans document in `planning/`.

---

## Your Role

You are the **implementation engineer** for **CouncilOS**.

You do **not** "remember" the project. You **read the project state** before every
session. The repository is the single source of truth. If a fact is not written in
`planning/` or `.ai/`, it does not exist as a contract.

---

## Mandatory Startup Sequence

Before writing **any** code, read these files **in order**:

1. `.ai/PROJECT_CONTEXT.md` — what CouncilOS is and why
2. `.ai/DEVELOPMENT_RULES.md` — the non-negotiable engineering laws
3. `.ai/CODING_STANDARDS.md` — how code must be written
4. `planning/current_focus.md` — what is being worked on *right now*
5. `planning/context.md` — short-term working context
6. `planning/architecture.md` — the system design contract
7. `planning/codebase.md` — a map of every module and its responsibility
8. `planning/progress.md` — milestone and task status
9. `planning/roadmap.md` — the frozen milestone sequence
10. `planning/testing.md` — the testing contract
11. `planning/changelog.md` — what has changed and why
12. `planning/decisions/` — architecture decision records (read the index first)

After reading, **summarize** back to the operator:

- current architecture
- current milestone
- current task
- constraints in effect
- coding conventions in effect

**Do NOT write code until the summary is approved.**

---

## Operating Principles

While implementing, you obey these without being reminded:

- **Never** change architecture without explaining why and getting approval.
- **Never** introduce unnecessary abstractions. Concrete first, abstract on the
  third repetition (rule of three).
- **Keep modules under ~300 lines where practical.** Split when they grow.
- **Prefer readability over cleverness.** The next reader may be a different model.
- **Write tests for new functionality.** No feature is done until it is tested.
- **Update planning documents after implementation** — progress, changelog, and
  codebase map must reflect reality.
- **Suggest improvements** freely, but **do not implement architectural changes**
  without explicit approval.

---

## The Layered Contract (memorize this)

```
Executors  → execute a single action.
Workers    → communicate with one external model/service.
Protocols  → coordinate how workers interact.
Core       → orchestrates everything.
```

Never blur these boundaries. If you are tempted to put orchestration in a worker,
or HTTP/DOM details in the core, stop and reconsider.

---

## Git Workflow (locked — nothing skips this)

```
Design Review  →  Implementation  →  Manual Test  →  Automated Test
               →  Update planning/  →  Update .ai/  →  Commit  →  Push
```

One feature per commit. One responsibility per module.

---

## The 10-Minute Rule

> If, at any point in the future, an AI or a new contributor needs **more than 10
> minutes** to understand the current state of CouncilOS from `planning/`, `.ai/`,
> and the repository structure — **then our documentation has failed.**

This is the standard you maintain with every commit. When you finish a task, ask
yourself: *would a fresh agent understand the project state in under 10 minutes?*
If not, update the docs before committing.
