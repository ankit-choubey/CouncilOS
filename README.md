# CouncilOS ⚖️

CouncilOS is an advanced multi-agent coordination and orchestration framework designed to manage complex, multi-perspective decision-making, automated reasoning, and collaborative task execution.

## 🌌 Overview

CouncilOS structures LLM-based agents into **Councils**—specialized assemblies where distinct agents act as advocates, critics, synthesizers, and judges. This framework moves beyond simple agent chaining, enabling complex debate, structured critique, consensus building, and rigorous evaluation protocols.

---

## 📂 Project Structure

```
CouncilOS/
│
├── planning/
│   ├── roadmap.md            # Long-term goal tracking and milestones
│   ├── architecture.md       # System design, data flow, and agent topologies
│   ├── decisions.md          # Architecture Decision Records (ADR)
│   ├── changelog.md          # Version history and release notes
│   ├── research_notes.md     # Reference materials and experimental ideas
│   └── session_logs/         # Saved debate and run logs
│
├── app/
│   ├── automation/           # Task scheduling, workflows, and event loops
│   ├── agents/               # Individual Agent definitions (Advocates, Critics, etc.)
│   ├── protocols/            # Debate structures, voting, and consensus mechanics
│   ├── memory/               # Short-term context and long-term semantic memory
│   ├── retrieval/            # Vector DB integrations and RAG pipelines
│   ├── judges/               # Evaluators, guardrails, and validation agents
│   ├── utils/                # Logging, configuration helpers, and shared utilities
│   └── main.py               # Application entry point
│
├── tests/                    # Unit, integration, and agent-interaction tests
├── logs/                     # Application execution logs
├── configs/                  # Environment and run configurations
│
├── requirements.txt          # Python dependencies
├── .env                      # Local secret variables
├── .gitignore                # Git exclusion patterns
├── README.md                 # Project introduction and documentation
└── setup.py                  # Installation and packaging script
```

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.10+
- Virtual Environment (recommended)

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/ankit-choubey/ai-council.git
cd CouncilOS
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 3. Configuration
Copy the environment template and fill in your API keys:
```bash
cp .env.example .env # Set your keys in .env
```

---

## 🧩 Core Architecture

CouncilOS relies on four fundamental components to orchestrate high-quality outcomes:

1. **The Council**: A collection of specialized agents convened to address a specific objective.
2. **Protocols**: Rules of order governing how agents speak, respond, vote, and build consensus.
3. **Memory**: Shared and private state spaces that allow agents to refer back to previous discussion turns.
4. **Judges**: Objective metric-based and LLM-based evaluators that determine when a decision meets the quality threshold.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
