# Prompt: Debug an Issue

> Use this when something is broken and needs systematic investigation.

---

We are debugging the following issue:

> **[DESCRIBE THE SYMPTOM: what happened, what was expected, how to reproduce]**

Investigate methodically. Do **not** start by changing code.

1. **Reproduce.** Confirm you can trigger the symptom. If you cannot, say so before
   going further.
2. **Localize.** Use logs, stack traces, and the codebase map in
   `planning/codebase.md` to narrow it to the smallest possible module/function.
   State the suspected location with `file:line`.
3. **Form a hypothesis.** One sentence: "I believe X because Y."
4. **Verify the hypothesis.** Add a failing test that reproduces the bug, or gather
   evidence (a log line, a value). Do not patch on a hunch.
5. **Fix the smallest correct change.** Prefer a targeted fix over a rewrite. Keep
   within the layered contract.
6. **Confirm.** The reproducing test now passes; the full suite still passes
   (`./scripts/test.sh`). Show output.
7. **Document.** Update `changelog.md`. If the root cause was architectural, write
   an ADR or a note in `planning/research_notes.md`.

Constraints:

- Never silence a failing test to make the suite green.
- Never broaden a `try/except` to swallow the symptom.
- If the bug reveals a contract gap, stop and surface it rather than papering over.
- Distinguish retryable failures (transient: network, DOM lag) from terminal ones
  (auth, schema mismatch) — the fix is different.
