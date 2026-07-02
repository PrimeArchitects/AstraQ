#!/usr/bin/env bash
# Blocks until Postgres, Redis, and the backend health endpoint are reachable.
# Useful in CI before running integration tests against the compose stack.
set -euo pipefail

echo "==> Waiting for Postgres"
until docker compose exec -T postgres pg_isready -U "${POSTGRES_USER:-astrasphere}" >/dev/null 2>&1; do
  sleep 1
done

echo "==> Waiting for Redis"
until docker compose exec -T redis redis-cli ping >/dev/null 2>&1; do
  sleep 1
done

echo "==> Waiting for backend health endpoint"
until curl -fs http://localhost:8000/api/v1/health >/dev/null 2>&1; do
  sleep 1
done

echo "==> All services ready"
