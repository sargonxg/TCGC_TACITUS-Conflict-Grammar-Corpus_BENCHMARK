#!/usr/bin/env bash
set -euo pipefail

echo "=== TCGC Bootstrap ==="

if ! command -v uv &>/dev/null; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "Syncing dependencies with uv..."
uv sync --all-extras --dev

echo "Installing pre-commit hooks..."
uv run pre-commit install

echo "Running test suite..."
uv run pytest -q --cov=tcgc --cov-fail-under=90

echo ""
echo "=== Bootstrap complete ==="
echo "See CONTRIBUTING.md for next steps."
echo "Docs: https://www.tacitus.me/research/tcgc"
