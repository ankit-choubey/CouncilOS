#!/usr/bin/env bash
# format.sh — format and lint the codebase.
# Runs black, isort, and ruff in that order.
set -euo pipefail

cd "$(dirname "$0")/.."

# shellcheck disable=SC1091
source .venv/bin/activate 2>/dev/null || true

echo ">> black"
black app tests

echo ">> isort"
isort app tests

echo ">> ruff"
ruff check app tests

echo ">> Done."
