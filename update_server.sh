#!/bin/bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_ROOT="$PROJECT_ROOT/templates"
VENV_PATH="$PROJECT_ROOT/.venv"

echo "==> Enter project directory"
cd "$PROJECT_ROOT"

echo "==> Pull latest code"
git pull --ff-only

echo "==> Update backend dependencies"
if [ ! -d "$VENV_PATH" ]; then
  python3 -m venv "$VENV_PATH"
fi

source "$VENV_PATH/bin/activate"
pip install --upgrade pip
pip install -r "$PROJECT_ROOT/requirements.txt"

echo "==> Update frontend dependencies"
cd "$FRONTEND_ROOT"
DEFAULT_NODE16_BIN="$HOME/miniconda3/envs/greaterwms_env/bin"
if [ -x "$DEFAULT_NODE16_BIN/node" ] && [ "${USE_BUNDLED_NODE16:-1}" = "1" ]; then
  export PATH="$DEFAULT_NODE16_BIN:$PATH"
fi

npm run check:node
npm ci

echo "==> Build frontend"
npm run build

echo "==> Restart services"
cd "$PROJECT_ROOT"
sudo systemctl restart greaterwms-frontend
sudo systemctl restart greaterwms-backend

echo "==> Service status"
sudo systemctl status greaterwms-frontend --no-pager
sudo systemctl status greaterwms-backend --no-pager

echo "==> Done"
echo "Frontend: http://49.233.206.226"
