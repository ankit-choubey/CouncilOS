# Research Notes & Experiments 🔬

Use this document to log brainstorming sessions, research papers, and experimental results for CouncilOS.

## 📚 Interesting Reading & References
- **"Generative Agents: Interactive Simulacra of Human Behavior" (Park et al.)** - Useful for architectural insights on agent memory and observation streams.
- **"More Agents, More Vote: Consensus in Multi-Agent Systems"** - Theoretical limits and properties of voting systems among LLMs.
- **"Self-Refine: Iterative Refinement with Self-Feedback" (Madaan et al.)** - Foundation for the Advocate-Critic debate architecture.

## 💡 Architectural Ideas to Explore
1. **Dynamic Council Size**: Automatically spawn more Critics or Specialists if the primary Judge flags high ambiguity or security risks in a proposal.
2. **Cognitive Refinement Loops**: Instead of sequential steps, run debate in parallel graphs using consensus-seeking algorithms.
3. **Optimized Embedding Cache**: Store past critiques and responses locally in a vector store to instantly guide agents away from previously identified flaws.
