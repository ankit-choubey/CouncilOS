#!/usr/bin/env bash
# setup.sh — one-shot project bootstrap.
# Creates the virtualenv, upgrades pip, installs the project + dev tooling,
# and prepares browser binaries if the browser extra is requested.
set -euo pipefail

cd "$(dirname "$0")/.."

PY="${PYTHON:-python3}"

echo ">> Creating virtual environment in .venv"
if [ ! -d .venv ]; then
  "$PY" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo ">> Upgrading pip"
python -m pip install --upgrade pip

echo ">> Installing project (dev extras)"
pip install -e ".[dev]"

# Optional: browser binaries (needed only for browser-backed workers, Milestone 3+)
if [ "${1:-}" = "--browser" ]; then
  echo ">> Installing browser extra + Playwright binaries"
  pip install -e ".[browser]"
  python -m playwright install chromium
fi

if [ ! -f .env ] && [ -f .env.example ]; then
  echo ">> Copying .env.example -> .env (fill in your keys)"
  cp .env.example .env
fi

echo ">> Setup complete. Activate with:  source .venv/bin/activate"
