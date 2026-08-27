#!/usr/bin/env bash
# Wrapper that routes uv run commands to the home-directory venv.
# Usage: ./scripts/run.sh sync
#        ./scripts/run.sh osmcp-serve
set -euo pipefail

export UV_PROJECT_ENVIRONMENT="$HOME/.venv/outsystems-mcp"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

exec uv run "$@"
