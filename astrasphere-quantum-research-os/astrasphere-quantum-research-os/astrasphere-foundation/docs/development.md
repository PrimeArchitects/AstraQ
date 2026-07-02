# Development Guide

## Daily workflow

```bash
make up          # start everything (idempotent — safe to leave running)
make logs         # tail all logs
make backend-shell   # shell into the backend container
make frontend-shell  # shell into the frontend container
```

Both `backend/` and `frontend/` are bind-mounted into their containers,
so edits on your host hot-reload inside the container — no rebuild
needed for code changes. A rebuild (`make build`) is only needed after
changing dependencies (`pyproject.toml`, `package.json`) or a
Dockerfile.

## Backend development

- **Add a new endpoint:** create a router in
  `app/api/v1/routers/`, register it in `app/api/v1/router.py`.
- **Add a model:** create it in `app/models/`, subclassing `Base` from
  `app/db/base.py`. Import it in `app/db/base_registry.py` so Alembic's
  autogenerate can see it.
- **Add a repository:** subclass `BaseRepository[YourModel]` in
  `app/repositories/`.
- **Add a service:** subclass `BaseService` in `app/services/`,
  composing one or more repositories via `__init__`. Routers depend on
  services, never on repositories directly.
- **Generate a migration:**
  ```bash
  make migrate-new name="add experiments table"
  make migrate
  ```
- **Run tests:** `make test-backend`, or inside the container:
  `pytest -v`, `pytest --cov=app`.
- **Lint/format:** `make lint`, `make format`, or inside the container:
  `ruff check . --fix`, `black .`, `mypy app`.

### Layering rules (enforced by convention, not tooling — review for these)

```
router → service → repository → ORM model
```

- Routers: HTTP concerns only (request/response, status codes, DI).
  Never import SQLAlchemy directly.
- Services: business logic. Never import FastAPI (`Request`,
  `HTTPException`, etc.) — raise `app.core.exceptions` types instead,
  which the middleware translates to HTTP responses.
- Repositories: the only layer allowed to write SQLAlchemy queries.
- Domain exceptions (`app/core/exceptions.py`) cross layer boundaries;
  HTTP-specific exceptions do not.

## Frontend development

- **Add a page:** create `src/app/<route>/page.tsx` (App Router
  convention — folder name is the URL segment).
- **Add a component:** shared UI primitives go in
  `src/components/ui/`; layout chrome in `src/components/layout/`;
  cross-cutting providers in `src/components/providers/`.
- **Add a shadcn/ui component:** `npx shadcn@latest add <component>`
  from `frontend/` — it reads `components.json` and drops the file into
  `src/components/ui/`.
- **Data fetching:** use TanStack Query (`useQuery`/`useMutation`) via
  the `QueryProvider` already wired into the root layout. Don't fetch
  in `useEffect`.
- **Styling:** Tailwind utility classes; design tokens (colors,
  fonts, animations) are defined once in `tailwind.config.ts` — extend
  that file rather than hardcoding hex values in components.
- **Lint/format:** `make lint`, `make format`, or inside the container:
  `npm run lint:fix`, `npm run format`.
- **Typecheck:** `npm run typecheck`.

## Git hooks

Husky + lint-staged run ESLint and Prettier on staged frontend files
before every commit (configured in `frontend/package.json` →
`lint-staged`, wired via `frontend/.husky/pre-commit`). Backend
equivalents (`ruff`, `black`) run via `.pre-commit-config.yaml` — install
with `pre-commit install` from the repo root if you also want backend
checks pre-commit rather than only in CI.

## Environment variables

Single source of truth: `app/core/config.py::Settings` (backend) and
`.env.example` files (both services). Add new config as a typed field
on `Settings` rather than reading `os.environ` ad hoc — misconfiguration
then fails at boot instead of at first use.

## CI

`.github/workflows/ci.yml` runs on every push/PR to `main`: backend
lint+typecheck+test against real Postgres/Redis service containers,
frontend lint+typecheck+build, then a final job builds both production
Docker images to catch Dockerfile regressions. All three must pass
before merge.
