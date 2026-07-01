#!/usr/bin/env bash
# test.sh — run the default (unit) test suite with coverage.
# Integration and browser tests are opt-in and NOT run here:
#   pytest -m integration
#   pytest -m browser
set -euo pipefail

cd "$(dirname "$0")/.."

# shellcheck disable=SC1091
source .venv/bin/activate 2>/dev/null || true

# Deselect opt-in markers so the default run stays fast, free, and hermetic.
pytest -m "not integration and not browser" "$@"
