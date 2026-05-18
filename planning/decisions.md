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
