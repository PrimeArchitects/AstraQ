# Installation Guide

## Prerequisites

| Tool           | Minimum version | Check with            |
| -------------- | ---------------- | ---------------------- |
| Docker         | 24.x              | `docker --version`      |
| Docker Compose | v2 (plugin)       | `docker compose version` |
| Git            | any recent        | `git --version`         |

Optional, only needed if you want to run services outside Docker:

| Tool   | Version | Notes                          |
| ------ | ------- | ------------------------------- |
| Node.js | 20.x    | Frontend, matches CI and Dockerfile |
| Python  | 3.12    | Backend, matches CI and Dockerfile  |

## 1. Clone and bootstrap

```bash
git clone <repo-url> astrasphere
cd astrasphere
make setup
```

`make setup` copies `.env.example` → `.env` at the root, and into
`backend/` and `frontend/` for local (non-Docker) runs. Open `.env` and
adjust values — the defaults work for local development out of the box.

## 2. Start the stack

```bash
make up
```

This builds and starts every service: `postgres`, `redis`, `qdrant`,
`backend`, `frontend`. First build takes a few minutes; subsequent
builds are cached.

Check status:

```bash
make ps
make logs
```

Verify:

- Frontend — http://localhost:3000 should show the console shell.
- Backend health — `curl http://localhost:8000/api/v1/health` should
  return `{"status": "ok", ...}`.
- API docs — http://localhost:8000/docs (Swagger UI, dev/staging only).

## 3. Apply database migrations

Applies the `users`/`sessions`/`user_preferences`/`auth_providers`
migration (see docs/authentication.md for the schema):

```bash
make migrate
```

## Running services outside Docker (optional)

**Backend:**

```bash
cd backend
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # point POSTGRES_HOST/REDIS_HOST/QDRANT_HOST at localhost
uvicorn app.main:app --reload
```

**Frontend:**

```bash
cd frontend
npm install
cp .env.example .env.local
npx auth secret       # writes a real AUTH_SECRET into .env.local
npm run dev
```

Google sign-in stays inactive until `GOOGLE_CLIENT_ID`/
`GOOGLE_CLIENT_SECRET` are set in both `frontend/.env.local` and
`backend/.env` — see docs/authentication.md "OAuth configuration".

You'll still need Postgres, Redis, and Qdrant reachable somewhere —
either run just those three via `docker compose up postgres redis
qdrant`, or point the env vars at existing instances.

## Troubleshooting

- **Port already in use** — another process is bound to 3000, 8000,
  5432, 6379, or 6333. Stop it, or change the mapped port in
  `docker-compose.yml`.
- **`docker compose` not found** — you likely have the old standalone
  `docker-compose` (with a hyphen) instead of the Compose v2 plugin.
  Install Docker Desktop or the `docker-compose-plugin` package.
- **Backend can't reach Postgres** — if running the backend outside
  Docker, make sure `POSTGRES_HOST=localhost` (not `postgres`, which
  only resolves inside the Compose network).
- **Stale containers after a Dockerfile change** — run `make build`
  to force a clean rebuild.
