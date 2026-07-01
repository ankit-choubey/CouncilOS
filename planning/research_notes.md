# Research Notes & Experiments

> Hard-won findings worth preserving across sessions. This is **not** a contract —
> it is reference material. When a note matures into a decision, it becomes an ADR.

---

## Carried over: browser automation for web-based LLMs

These findings come from the pre-restructure prototype (a Playwright-driven ChatGPT
client). The code was removed, but the lessons feed **Milestone 3 (ChatGPT Worker)**
and any future browser-executor-backed worker. Do not rediscover them from scratch.

### 1. Browser profile persistence & anti-detection
- **Problem:** A default headless Chromium triggers anti-bot challenges (e.g.
  Cloudflare) and forces a manual email/2FA login on every run.
- **What worked:**
  - Launch with a **persistent user-data directory** (`profiles/<model>`) so cookies,
    localStorage, and login state survive across runs.
  - Run **`headless=False`** during core operations — it matches a real user's
    fingerprint (canvas/WebGL) and avoids bot detection.
- **Implication for M3:** the ChatGPT worker's executor should mount a persistent
  context dir per model and default to headed mode for reliability.

### 2. DOM-based streaming text stabilization
- **Problem:** ChatGPT streams tokens over SSE into the DOM. Reading immediately
  after "send" returns truncated text.
- **What worked — a tick-based stabilization loop:**
  1. Locate the latest assistant node, e.g. `[data-message-author-role="assistant"]`
     via `.nth(count - 1)`.
  2. Read its `inner_text()`.
  3. Wait a short interval (prototype used `2.0s`).
  4. Read again. If unchanged and non-empty, streaming has finished.
- **Why it beat alternatives:** lighter than a `MutationObserver` injection,
  resilient to latency spikes, decoupled from network sniffing.
- **Implication for M2/M3:** a browser executor's "read response" action should
  expose a configurable stabilization policy. The worker (not the executor) should
  decide when "done" is acceptable.

### 3. Selectors as a registry
- **Problem:** web UIs change; hardcoding selectors in logic makes it brittle.
- **What worked:** a single decoupled selector map per target (`prompt_box`,
  `send_button`, assistant node). When the UI changes, only the map is patched.
- **Implication:** each browser-backed worker owns its own selector map; it never
  leaks into protocols or core.

---

## Reading list (background)

- **Generative Agents (Park et al.)** — agent memory and observation streams.
- **Self-Refine (Madaan et al.)** — iterative critique/refine; relevant to judging.
- **More Agents, More Vote** — properties/limits of voting among LLMs.

---

## Ideas to explore (not committed)

- **Dynamic council size:** spawn extra workers if the judge flags high ambiguity.
- **Embedding cache of past critiques:** steer agents away from known-bad paths.
- **Parallel debate graphs** instead of sequential round-robin.

These are noted for the future; they are out of scope until after Milestone 9.
