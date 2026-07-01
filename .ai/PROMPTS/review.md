# Prompt: Review a Pull Request / Change

> Use this to have the agent review its own work or a diff before it is committed/merged.

---

Review the following change as a strict but fair engineer. The change is:

> **[PASTE THE DIFF, THE PR URL, OR POINT TO THE BRANCH/COMMIT]**

Check it against the CouncilOS laws and standards. Be specific — cite file:line.

**Architecture & contract**
- [ ] Does it respect the layered contract? (Executors execute, Workers communicate,
      Protocols coordinate, Core orchestrates.)
- [ ] Is any model-specific behavior leaking out of a worker?
- [ ] Does it introduce an abstraction that isn't justified yet?

**Correctness**
- [ ] Are there edge cases unhandled (empty input, timeout, auth failure)?
- [ ] Are failure modes classified (retryable vs terminal)?
- [ ] Are types complete and `mypy --strict`-clean?

**Quality**
- [ ] Is each module under ~300 lines and single-responsibility?
- [ ] Are names intention-revealing? Any `tmp`, `x`, dead code, commented-out blocks?
- [ ] Does it follow the formatting/lint config (black, isort, ruff)?

**Tests**
- [ ] Does new functionality have tests?
- [ ] Do unit tests avoid the network? Are live/browser tests opt-in?
- [ ] Do the tests describe behavior, not implementation?

**Documentation**
- [ ] Do `progress.md`, `changelog.md`, `codebase.md` reflect the change?
- [ ] If the change touched an open design question, is there a new ADR?
- [ ] Would a fresh agent understand the project state in under 10 minutes after
      this change?

Output format:

1. **Verdict:** approve / request changes / block
2. **Must-fix** (blocking, with file:line and reason)
3. **Should-fix** (non-blocking)
4. **Nits** (optional)
