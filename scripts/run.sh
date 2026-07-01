#!/usr/bin/env bash
# run.sh — run the CouncilOS core entry point.
# (No entry point exists until Milestone 1+; this is a placeholder that will be
# wired to app.cli:main once it lands.)
set -euo pipefail

cd "$(dirname "$0")/.."

# shellcheck disable=SC1091
source .venv/bin/activate 2>/dev/null || true

echo ">> No CLI entry point yet (lands in Milestone 1+)."
echo ">> This script will eventually run: python -m app.cli"
