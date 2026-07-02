#!/usr/bin/env bash
# First-time environment bootstrap: env files, dependency checks, git hooks.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Checking required tools"
for cmd in docker git; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "Missing required tool: $cmd"; exit 1; }
done
docker compose version >/dev/null 2>&1 || { echo "docker compose plugin not found"; exit 1; }

echo "==> Creating environment files"
[ -f .env ] || cp .env.example .env
[ -f backend/.env ] || cp backend/.env.example backend/.env
[ -f frontend/.env.local ] || cp frontend/.env.example frontend/.env.local

if [ -d .git ]; then
  echo "==> Installing git hooks (Husky)"
  (cd frontend && npm install && npx husky init >/dev/null 2>&1 || true)
fi

echo "==> Bootstrap complete. Next: make up"
