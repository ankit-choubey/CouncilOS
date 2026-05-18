# CouncilOS Roadmap 🗺️

This document outlines the roadmap and future milestones for CouncilOS.

---

## 🚀 Phase 1: Core Architecture & Single-Turn Debate (Q2 2026)
- [x] **Establish Modular Package Layout** (App directories, core configurations, and modular package architecture).
- [x] **Implement Web Automation Interface** (Playwright browser driver, CSS selectors registry, `ChatGPTClient`, and real-time DOM stream polling for stabilized prompt responses).
- [x] **Integrate Observability System** (Shared color-coded terminal console logs via Rich logging utilities).
- [ ] **Define Agent Abstractions** (`BaseAgent`, `Advocate`, `Critic`) and bind their core generation steps to the browser execution pipelines.
- [ ] **Implement State Space & Memory Context** (`DebateContext`) to store local variables and serialize debate state.
- [ ] **Build Single-Turn Debate Engine** (Orchestrate a single-round debate: 1 Advocate proposes, 1 Critic highlights flaws, 1 Judge rules).
- [ ] **Create Judge Evaluation Metrics** (Formulate criteria scoring safety, completeness, accuracy, and consensus).

---

## 👥 Phase 2: Multi-Agent Councils & Dynamic Protocols (Q3 2026)
- [ ] **Support Multi-Round Debates** (Turn-taking coordination loops and dynamic debate progression).
- [ ] **Implement Voting & Consensus Protocols** (Support majority votes, Elo-based scaling, and agent synthesizers).
- [ ] **Integrate Cognitive Tools** (Support external search, vector storage, and RAG architectures for agent citing).
- [ ] **Add Dashboard / UI Interface** (Launch an interactive visualization app to track debate graphs in real-time).

---

## 🧠 Phase 3: Advanced Cognitive Models & Evaluation (Q4 2026)
- [ ] **Implement Long-Term Episodic Memory** (Maintain past debates in persistent vectorized episodic database layers).
- [ ] **Configure Red Teaming Protocols** (Formulate alignment-testing routines and safety boundary verification tests).
- [ ] **Evaluate Benchmarking Suites** (Run evaluation suites against standard AI reasoning models using datasets like MMLU, GSM8K).
- [ ] **Deploy Production Wrappers** (Package CouncilOS inside Docker environments and provide standard FastAPI endpoints).
