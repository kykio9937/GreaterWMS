#!/bin/bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_ROOT="$PROJECT_ROOT/templates"
DEFAULT_NODE16_BIN="$HOME/miniconda3/envs/greaterwms_env/bin"

if [ -x "$DEFAULT_NODE16_BIN/node" ] && [ "${USE_BUNDLED_NODE16:-1}" = "1" ]; then
  export PATH="$DEFAULT_NODE16_BIN:$PATH"
fi

cd "$FRONTEND_ROOT"
npm run build
exec npm run start
