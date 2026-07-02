# AstraSphere Quantum Research OS

A production-ready, full-stack operating system for quantum computing research teams —
project tracking, semantic literature search, and experiment coordination behind a single
clean-architecture platform.

## Tech Stack

| Layer          | Technology                                             |
| -------------- | ------------------------------------------------------- |
| Frontend       | Next.js 15 (App Router), TypeScript, Tailwind CSS       |
| Backend        | FastAPI (Python 3.12), SQLAlchemy 2.0 (async), Pydantic |
| Relational DB  | PostgreSQL 16                                            |
| Cache / Queue  | Redis 7                                                  |
| Vector Search  | Qdrant                                                   |
| Infra          | Docker, Docker Compose                                   |
| CI             | GitHub Actions                                           |

## Architecture

```
astrasphere-quantum-research-os/
├── frontend/                # Next.js App Router (TypeScript + Tailwind)
│   └── src/
│       ├── app/              # Routes, layouts, pages, API routes
│       ├── components/       # Reusable UI components
│       ├── lib/               # API client, utilities
│       └── types/             # Shared TypeScript types
│
├── backend/                 # FastAPI service (clean/layered architecture)
│   └── app/
│       ├── api/               # Route handlers (v1, versioned)
│       ├── core/              # Config, logging, security
│       ├── db/                 # Engine/session management
│       ├── models/             # SQLAlchemy ORM models
│       ├── schemas/            # Pydantic request/response schemas
│       └── services/           # Redis, Qdrant integration clients
│   ├── alembic/               # Database migrations
│   └── tests/                  # Pytest test suite
│
├── docker-compose.yml        # Orchestrates all services
└── .github/workflows/ci.yml  # Lint, typecheck, test, build pipeline
```

The backend follows a **layered clean architecture**: API handlers depend on services and
the database session via dependency injection, domain models are isolated from transport
schemas (ORM models vs. Pydantic schemas), and configuration is centralized in
`app/core/config.py`. This keeps business logic testable independent of FastAPI or the
database driver.

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 22+ (for local frontend development outside Docker)
- Python 3.12+ (for local backend development outside Docker)

### Quick Start (Docker Compose)

```bash
# 1. Copy environment configuration
cp .env.example .env

# 2. Build and start every service
docker compose up --build

# Frontend  → http://localhost:3000
# Backend   → http://localhost:8000
# API docs  → http://localhost:8000/api/v1/docs
# Qdrant UI → http://localhost:6333/dashboard
```

The backend automatically waits for Postgres and Redis to become healthy before starting,
and creates the Qdrant collection on boot.

### Running Database Migrations

```bash
docker compose exec backend alembic upgrade head
```

### Local Development (without Docker)

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env   # point DATABASE_URL/REDIS_URL/QDRANT_URL at localhost
uvicorn app.main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## Testing

```bash
# Backend
cd backend && pytest --cov=app

# Frontend
cd frontend && npm run test
```

## Linting & Formatting

```bash
# Backend
cd backend && ruff check . && black --check . && mypy app

# Frontend
cd frontend && npm run lint && npm run format:check && npm run typecheck
```

## Logging

The backend uses [`structlog`](https://www.structlog.org/) for structured logging —
JSON-formatted in production, human-readable console output in development. All log lines
are contextual (e.g. `research_project.created`, `vector_search.executed`) to support
log-based alerting and tracing.

## API Overview

| Method   | Endpoint                     | Description                          |
| -------- | ----------------------------- | ------------------------------------- |
| `GET`    | `/api/v1/health`              | Liveness probe                        |
| `GET`    | `/api/v1/health/ready`        | Readiness probe (Postgres/Redis/Qdrant) |
| `GET`    | `/api/v1/research`            | List research projects                |
| `POST`   | `/api/v1/research`            | Create a research project             |
| `GET`    | `/api/v1/research/{id}`       | Retrieve a research project           |
| `PATCH`  | `/api/v1/research/{id}`       | Update a research project             |
| `DELETE` | `/api/v1/research/{id}`       | Delete a research project             |
| `POST`   | `/api/v1/vectors/search`      | Semantic search over embedded documents |

Full interactive documentation is available at `/api/v1/docs` (Swagger UI) and
`/api/v1/redoc` once the backend is running.

## Environment Configuration

All configuration is environment-variable driven. See `.env.example` at the repo root,
`backend/.env.example`, and `frontend/.env.example` for the full list of variables. Secrets
(`SECRET_KEY`, database passwords) must be overridden before any non-local deployment.

## CI/CD

`.github/workflows/ci.yml` runs on every push and pull request to `main`:

1. **Backend job** — ruff lint, black format check, mypy type check, pytest with coverage
   (against real Postgres/Redis service containers).
2. **Frontend job** — ESLint, TypeScript check, Prettier check, Vitest unit tests, production
   build.
3. **Docker build job** — sanity-builds both Docker images to catch Dockerfile regressions.

## Notes on Production Hardening

This scaffold is production-oriented but a few items are intentionally left as follow-ups
for a real deployment:

- Replace the placeholder embedding function in `app/api/v1/endpoints/vectors.py` with a
  real embedding model/provider.
- Add authentication (JWT scaffolding is included in `app/core/security.py`) and wire it
  into protected routes.
- Configure TLS termination and a reverse proxy (e.g. Caddy/Traefik/Nginx) in front of the
  Compose stack for non-local environments.
- Point `BACKEND_CORS_ORIGINS` and `NEXT_PUBLIC_API_BASE_URL` at real domains.

## License

MIT — see `LICENSE` (add your organization's license terms before publishing).
