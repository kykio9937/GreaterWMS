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
npm install

echo "==> Build frontend"
export NODE_OPTIONS=--openssl-legacy-provider
npx quasar build

echo "==> Restart services"
cd "$PROJECT_ROOT"
sudo systemctl restart greaterwms-frontend
sudo systemctl restart greaterwms-backend

echo "==> Service status"
sudo systemctl status greaterwms-frontend --no-pager
sudo systemctl status greaterwms-backend --no-pager

echo "==> Done"
echo "Frontend: http://49.233.206.226"
