# DEVELOPMENT_RULES.md — The Engineering Laws of CouncilOS

> These are **laws**, not guidelines. They are permanent. An AI implementer that
> breaks one must explain why, in writing, before proceeding.

---

1. **Architecture before implementation.**
   No production code is written until the relevant piece of the architecture is
   agreed and recorded.

2. **One feature per commit.**
   A commit does exactly one thing. "While I was in there" changes go in a separate
   commit — or, better, a separate branch.

3. **One responsibility per module.**
   If you cannot describe a module's job in one sentence, it has two jobs. Split it.

4. **Every new feature requires tests.**
   No feature is "done" until it has a test. Untested code is unfinished code.

5. **Update planning docs after successful implementation.**
   `planning/progress.md`, `planning/changelog.md`, and `planning/codebase.md`
   must reflect reality after every change. The repo is the source of truth.

6. **Do not duplicate logic.**
   If logic appears twice, extract it. If it appears a third time, refactor now.

7. **Never hardcode model-specific behavior outside workers.**
   ChatGPT selectors, Gemini SDK quirks, Perplexity auth — all stay inside their
   worker. Core, protocols, and executors are vendor-agnostic. Always.

8. **Respect the layered contract.**
   ```
   Executors execute.  Workers communicate.  Protocols coordinate.  Core orchestrates.
   ```
   Do not put orchestration in a worker. Do not put HTTP/DOM detail in the core.
   Do not put cross-worker coordination in a protocol that an executor calls.

9. **Prefer interfaces over assumptions.**
   Code against the abstract `Worker` (or `Executor`, `Protocol`), never against a
   concrete ChatGPT worker, unless you are inside its own module or its tests.

10. **Explain tradeoffs before large refactors.**
    A refactor touching more than ~2 modules requires a written rationale and
    approval, recorded as an ADR in `planning/decisions/`.

---

## Supporting habits

- **Concrete first, abstract on the third repetition.** Don't pre-build frameworks.
- **Read before write.** Re-read the affected module and its tests before editing.
- **Small steps.** Implement → run → commit. Don't accumulate 300 lines unverified.
- **Leave the campsite cleaner.** If you touch a module, fix the typos and dead code
  you pass on the way — but in a separate commit (see rule 2).
- **When in doubt, ask.** An AI implementer never silently makes an architectural
  decision. Surface it; get approval; record it.
