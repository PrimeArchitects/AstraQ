#!/usr/bin/env bash
# Applies pending Alembic migrations against the running backend container.
set -euo pipefail
docker compose exec backend alembic upgrade head
