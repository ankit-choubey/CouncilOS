# Changelog 📋

All notable changes to the CouncilOS project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-19

### Added
- **Browser Automation Infrastructure** (`app/automation/`):
  - Created `BrowserManager` using asynchronous Playwright to spin up persistent, non-headless Chromium contexts with local user data caching in `profiles/chatgpt` (retaining sessions and reducing authentication friction).
  - Implemented `ChatGPTClient` to programmatically control prompt injection, locator targeting, and page navigation on `https://chatgpt.com`.
  - Added a **DOM Polling & Stream Stabilization algorithm** inside `ChatGPTClient` that compares sequential inner text updates of assistant message blocks at a 2-second interval, ensuring complete text payload extraction once token streaming stops.
  - Implemented a decoupled selectors dictionary `selectors.py` housing CSS selectors (`prompt_box`, `send_button`) to support rapid web-interface layout patching.
- **Observability & Logging Utilities** (`app/utils/`):
  - Created `logger.py` utilizing the premium `rich` terminal library to instantiate a shared, color-coded console logging pipeline.
- **Application Execution Pipeline** (`app/main.py`):
  - Orchestrated browser initialization, user CLI prompt capture, async browser client interaction, progress monitoring, formatted response rendering, and graceful cleanup to prevent stray Chromium processes.
- **Initial Workspace Layout**:
  - Structured modular package layouts for `agents`, `protocols`, `memory`, `retrieval`, `judges`, and `utils` under `app/`.
  - Added root configurations (`README.md`, `.gitignore`, `requirements.txt`, `.env`, `setup.py`).
  - Added full roadmap and architecture design documentation.
