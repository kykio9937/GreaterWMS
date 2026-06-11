#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
API_BASE_URL="${1:-}"

cd "$PROJECT_ROOT"

if [ -n "$API_BASE_URL" ]; then
  printf '%s\n' "$API_BASE_URL" > "$PROJECT_ROOT/templates/public/statics/baseurl.txt"
  if [ -f "$PROJECT_ROOT/templates/dist/spa/statics/baseurl.txt" ]; then
    printf '%s\n' "$API_BASE_URL" > "$PROJECT_ROOT/templates/dist/spa/statics/baseurl.txt"
  fi
  echo "API 地址已切换为: $API_BASE_URL"
fi

docker compose -f docker-compose.demo.yml up -d --build

echo "演示版服务已启动"
echo "前端: http://127.0.0.1:8080/#/"
echo "后端: http://127.0.0.1:8008"
