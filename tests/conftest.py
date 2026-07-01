"""Shared pytest fixtures and configuration for CouncilOS.

See planning/testing.md for the testing contract. This file is intentionally
minimal for Milestone 0; layer-specific fixtures (fake workers/executors) are
added as their contracts land in Milestones 1–2.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure the package root is importable when running without an editable install.
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
