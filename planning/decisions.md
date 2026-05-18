# Architecture Decision Records (ADR) 📝

This document records the architectural decisions made during the design and development of CouncilOS.

## ADR Template
Every ADR should follow this structure:
```markdown
### ADR-XXX: [Title]
* **Status**: [Draft / Proposed / Accepted / Superseded]
* **Date**: YYYY-MM-DD
* **Context**: [What is the problem and its constraints?]
* **Decision**: [What did we decide to do?]
* **Consequences**: [What are the benefits, trade-offs, and downfalls of this decision?]
```

---

## Records

### ADR-001: Project Layout and Base Structure
* **Status**: Accepted
* **Date**: 2026-05-19
* **Context**: The project needs a highly structured workspace that decouples agent behaviors, evaluation logic (judges), memory management, and automated pipelines, while preserving clean planning and documentation channels.
* **Decision**: We adopted a modular package structure in `app/`, paired with a comprehensive root `planning/` directory for system design, roadmap tracking, changelogs, and ADRs.
* **Consequences**:
  - Provides a clean separation of concerns for multi-agent development.
  - Simplifies automated testing in `tests/`.
  - Promotes comprehensive, living documentation inside `planning/`.

---

### ADR-002: Browser Automation for Web-Based LLM Integration 🚀 [NEW]
* **Status**: Accepted
* **Date**: 2026-05-19
* **Context**: 
  CouncilOS needs a robust, interactive channel to execute agent reasoning loops on advanced foundation models like ChatGPT. Direct REST API calls (OpenAI API, etc.) require separate API keys, pay-per-token pricing, and lack session persistence. To facilitate developer testing, support visual session persistence, and enable agent interaction with realistic user-facing web environments, we need a way to run interactions directly in a standard browser session.
* **Decision**:
  We built a dedicated **Browser Automation Layer** using asynchronous **Playwright** (`app/automation`). The system spins up Chromium contexts configured with a persistent user data directory (`profiles/chatgpt`) to cache cookies, authentication states, and settings. A specialized client (`ChatGPTClient`) drives the DOM elements, submitting prompts and utilizing a custom polling algorithm to detect when streaming responses stabilize.
* **Consequences**:
  - **Benefits**:
    - Zero cost per token during development and testing loops.
    - Persistent context retention (retains chat history in the user's browser account for auditability).
    - True interactive capability, allowing humans to step in and inspect the browser screen if needed.
    - Solid encapsulation: CSS selector changes only require patching a single registry (`selectors.py`).
  - **Trade-offs & Downfalls**:
    - Vulnerability to remote DOM changes (mitigated by decoupling selectors).
    - Slower response delivery compared to pure, stream-parsed JSON APIs.
    - Increased memory consumption from running a full Chromium browser process.
    - Requires system-level installation of Playwright browser binaries.
