# System Architecture & Design 🏗️

This document describes the structural design of CouncilOS.

## 🌀 High-Level Architecture

CouncilOS is built upon the concept of **Collaborative Multi-Agent Debates**. The goal is to maximize decision-making quality by organizing agents into structured, multi-role assemblies.

```
                  ┌────────────────────────┐
                  │      User Request      │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │    Debate Orchestrator │
                  └─────┬────────────┬─────┘
                        │            │
         ┌──────────────┘            └──────────────┐
         ▼                                          ▼
┌─────────────────┐                        ┌─────────────────┐
│  Advocate Agent │ ◄────────────────────► │   Critic Agent  │
│  (Proposes)     │       Debate           │  (Critiques)    │
└────────┬────────┘      Protocol          └────────┬────────┘
         │                                          │
         └──────────────┬────────────┬──────────────┘
                        │            │
                        ▼            ▼
                  ┌─────────┐    ┌─────────┐
                  │ Memory  │    │ Vector  │
                  │ Log     │    │ DB      │
                  └────┬────┘    └─────────┘
                       │
                       ▼
                  ┌─────────┐
                  │ Judge   │
                  │ Agent   │
                  └────┬────┘
                       │
                       ▼
                  ┌─────────┐
                  │ Final   │
                  │ Verdict │
                  └─────────┘
```

## 🧱 Core Modules

### 1. Agents (`app.agents`)
- **BaseAgent**: Foundation class managing basic message loop, prompt injection, and LLM call logic.
- **Advocate**: Optimized to propose plans, answer user prompts affirmatively, and provide justifications.
- **Critic**: Specialized in finding flaws, edge cases, risks, and logical inconsistencies in proposals.

### 2. Protocols (`app.protocols`)
- Defines rules of order. It manages the phase transitions (e.g., Proposal -> Critique -> Rebuttal -> Judgment).
- Determines how agents access context and memory.

### 3. Memory (`app.memory`)
- **DebateContext**: Ephemeral, structured context storing messages exchanged within the current debate session.
- **EpisodicMemory**: Storage of past debates to let the system learn from past successes/failures.

### 4. Judges (`app.judges`)
- Evaluates transcripts based on safety, completeness, accuracy, and consensus.
- Acts as a termination condition controller.
