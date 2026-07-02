# AstraSphere Quantum Research OS

An AI-powered research operating system for quantum computing labs,
universities, startups, and enterprise R&D teams.

> **Status: Foundation phase.** This repository currently contains the
> production-grade scaffolding — architecture, tooling, and infrastructure —
> with no business features yet. See [docs/architecture.md](docs/architecture.md)
> for what's here and what's intentionally not.

## Stack

| Layer          | Technology                                                   |
| -------------- | ------------------------------------------------------------- |
| Frontend       | Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query |
| Backend        | FastAPI, Python 3.12, SQLAlchemy 2.0 (async), Alembic, Pydantic v2 |
| Databases      | PostgreSQL, Redis, Qdrant                                     |
| Infrastructure | Docker, Docker Compose, GitHub Actions                        |

## Quick start

```bash
git clone <repo-url> astrasphere && cd astrasphere
make setup   # copies .env files
make up      # builds and starts the full stack
```

- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Backend health check: http://localhost:8000/api/v1/health

Full instructions, prerequisites, and troubleshooting: [docs/installation.md](docs/installation.md).

## Repository layout

```
astrasphere/
├── frontend/          Next.js application
├── backend/           FastAPI application
├── infrastructure/    Deployment infra (staging/production — reserved)
├── shared/            Cross-service contracts (e.g. OpenAPI schema)
├── docker/            Auxiliary Docker assets (see docker/README.md)
├── docs/              Documentation
├── scripts/           Bootstrap and operational scripts
├── tests/             Cross-service integration tests
├── .github/workflows/ CI pipelines
├── docker-compose.yml Local development stack
└── Makefile           Developer workflow shortcuts
```

Full explanation of every directory: [docs/architecture.md](docs/architecture.md).

## Documentation

- [Installation Guide](docs/installation.md) — prerequisites, setup, running locally
- [Development Guide](docs/development.md) — day-to-day workflow, testing, migrations
- [Architecture](docs/architecture.md) — design decisions, layer boundaries, extension points
- [Contributing](docs/contributing.md) — branching, commit conventions, review process

## What's deliberately not here yet

Authentication, AI features, and business logic are out of scope for
this phase by design — see the objective in
[docs/architecture.md](docs/architecture.md#foundation-scope). The
interfaces they'll plug into (`app/api/deps.py::get_current_user`,
`app/ai/provider.py::AIProvider`) already exist so later work extends
the scaffold rather than restructuring it.

## License

Proprietary — all rights reserved, unless a `LICENSE` file says
otherwise.
