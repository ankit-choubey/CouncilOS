# Prompt: Implement a Feature

> Use this after the bootstrap summary is approved and a specific feature is on deck.

---

We are implementing the following task (from `planning/current_focus.md`):

> **[PASTE THE SPECIFIC TASK HERE]**

Before you start:

1. Re-read `planning/architecture.md` and confirm this task fits the layered contract.
2. Re-read `planning/codebase.md` to find the module(s) this touches.
3. Check `planning/decisions/` for any ADR that governs the approach.
4. If anything is ambiguous or unspecified, **stop and ask** — do not invent
   architecture.

Then, following the locked git workflow:

1. **Design** — describe the change in 3–6 bullets: which modules, what new types,
   what new tests. Get approval before coding.
2. **Implement** — write the code. Annotate types. Keep files under ~300 lines.
3. **Manual test** — run it and show output.
4. **Automated test** — add/extend tests; run `./scripts/test.sh`; show the result.
5. **Update planning/** — update `progress.md`, `changelog.md`, `codebase.md` so
   they reflect the new reality. If the task resolved an open design question,
   write an ADR in `planning/decisions/`.
6. **Update .ai/** — only if a convention, rule, or contract changed.
7. **Commit** — one feature per commit, message in the form
   `Add <thing>` / `Fix <thing>` / `Refactor <thing>`. Do not push unless asked.

Hard rules for this session:

- Do not change architecture without explaining why and getting explicit approval.
- Do not introduce abstractions beyond what this task requires (rule of three).
- Do not hardcode model-specific behavior outside the relevant worker.
- Do not mark the task done until tests pass and docs are updated.
