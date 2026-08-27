#!/usr/bin/env bash
# Move the project venv out of iCloud-synced Documents into ~/.venv/outsystems-mcp
# Run once from the project root: bash scripts/setup-venv.sh
set -euo pipefail

VENV_PATH="$HOME/.venv/outsystems-mcp"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==> Project root: $PROJECT_ROOT"
echo "==> Target venv:  $VENV_PATH"

# Remove stale in-repo .venv (lives on iCloud — causes 'no module' errors)
if [[ -d "$PROJECT_ROOT/.venv" ]]; then
    echo "==> Removing stale .venv from project dir..."
    rm -rf "$PROJECT_ROOT/.venv"
fi

# Create the home-directory venv and install the project
export UV_PROJECT_ENVIRONMENT="$VENV_PATH"
cd "$PROJECT_ROOT"
echo "==> Running uv sync into $VENV_PATH ..."
uv sync

echo ""
echo "Done. Run commands with:"
echo "  UV_PROJECT_ENVIRONMENT=$VENV_PATH uv run sync"
echo "  UV_PROJECT_ENVIRONMENT=$VENV_PATH uv run osmcp-serve"
echo ""
echo "Or use the wrapper: ./scripts/run.sh sync"
