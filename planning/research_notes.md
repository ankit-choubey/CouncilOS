# Research Notes & Experiments 🔬

Use this document to log brainstorming sessions, research papers, and experimental results for CouncilOS.

---

## 📚 Interesting Reading & References
- **"Generative Agents: Interactive Simulacra of Human Behavior" (Park et al.)** - Useful for architectural insights on agent memory and observation streams.
- **"More Agents, More Vote: Consensus in Multi-Agent Systems"** - Theoretical limits and properties of voting systems among LLMs.
- **"Self-Refine: Iterative Refinement with Self-Feedback" (Madaan et al.)** - Foundation for the Advocate-Critic debate architecture.

---

## 💡 Architectural Ideas to Explore
1. **Dynamic Council Size**: Automatically spawn more Critics or Specialists if the primary Judge flags high ambiguity or security risks in a proposal.
2. **Cognitive Refinement Loops**: Instead of sequential steps, run debate in parallel graphs using consensus-seeking algorithms.
3. **Optimized Embedding Cache**: Store past critiques and responses locally in a vector store to instantly guide agents away from previously identified flaws.

---

## 🔬 Web Automation & Dynamic Scraper Experiments 🚀 [NEW]

During the implementation of the automation layer (`app/automation`), we researched and resolved two core challenges in web-scraping dynamic single-page LLM apps:

### 1. Browser Profile Persistence & Anti-Detection
- **Problem**: Launching a default headless Chromium instance triggers anti-bot mechanisms (like Cloudflare Turnstile) and requires users to manually complete multi-factor email/password logins on every test run.
- **Solution**: We implemented persistent context directory mounting (`profiles/chatgpt`). 
- **Findings**:
  - Setting `headless=False` during core operations simulates standard user behavior and prevents Canvas/WebGl fingerprint mismatch detection.
  - Persisting storage/session states under a local path ensures login cookies and OpenAI local storage configurations remain intact across program execution cycles.

### 2. DOM-Based Streaming Text Stabilization
- **Problem**: ChatGPT streams responses using Server-Sent Events (SSE), adding tokens dynamically to the DOM. Standard locator evaluations extract incomplete, truncated sentences because the scraper triggers immediately after the send action completes.
- **Solution**: Designed an asynchronous tick-based stabilization loop:
  - Locate the latest assistant response container: `[data-message-author-role="assistant"]` using `.nth(count - 1)`.
  - Fetch the `inner_text()` string.
  - Wait for an evaluation period (`2.0` seconds).
  - Compare the newly fetched `inner_text` string with the previous snapshot.
  - **Verdict**: If the text matches exactly and is non-empty, the LLM has stopped streaming, and the token generation is marked as complete.
- **Benefits**: Lightweight alternative to complex JS `MutationObserver` injections, highly resilient to latency spikes, and completely decoupled from browser network socket sniffing.
