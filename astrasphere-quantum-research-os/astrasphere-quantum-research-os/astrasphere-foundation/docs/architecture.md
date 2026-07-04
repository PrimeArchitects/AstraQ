# Architecture

## Foundation scope

This repository started as a foundation-only phase and has since grown
real features. As of this phase:

- **Authentication** — fully implemented. See
  [docs/authentication.md](authentication.md) for the complete
  architecture (self-hosted JWT/session auth in FastAPI, Auth.js as the
  frontend session layer, Google OAuth wired but inert until real
  credentials are provided).
- **AI features** — still a placeholder. `app/ai/provider.py::AIProvider`
  defines the contract (`complete`, `embed`); `NullAIProvider` is the
  only implementation and raises `NotImplementedError`. An
  Anthropic-backed implementation is a drop-in later, not a refactor.
- **PDF processing / research business logic** — no domain models or
  feature routers beyond auth/users/health exist yet.

## Why this stack

| Choice | Reasoning |
| --- | --- |
| **Next.js 15 App Router** | Server Components by default reduce client JS for a data-dense research console; file-based routing keeps the feature-first structure honest. |
| **FastAPI** | Async-native (matters for a backend that will proxy to Postgres, Redis, Qdrant, and external AI APIs concurrently), Pydantic-based validation gives free request/response schemas and OpenAPI docs. |
| **SQLAlchemy 2.0 (async) + Alembic** | Async ORM matches FastAPI's async model end to end — no sync DB calls blocking the event loop; Alembic gives reviewable, reversible schema migrations. |
| **PostgreSQL** | Relational integrity for research metadata (experiments, users, permissions) where correctness matters more than raw throughput. |
| **Redis** | Caching and, later, task queue / rate limiting — needed regardless of which AI or job-processing features come next. |
| **Qdrant** | Vector store for the AI/RAG layer (semantic search over papers, datasets, lab notebooks) that this scaffold intentionally defers but wires a connection point for. |
| **Tailwind + shadcn/ui** | Utility-first styling with copy-in (not npm-locked) component primitives — the design system stays editable rather than fighting an opaque component library. |
| **TanStack Query** | Server-state caching/invalidation on the client, so feature teams don't hand-roll fetch/loading/error state per component. |
| **Docker Compose** | One command reproduces the full stack (all three data stores + both apps) for local dev and CI, without requiring anyone to install Postgres/Redis/Qdrant natively. |

## Backend layering (Clean Architecture)

```
┌─────────────────────────────────────────┐
│ Routers (app/api/v1/routers/)            │  HTTP only: request/response, status codes
├─────────────────────────────────────────┤
│ Services (app/services/)                 │  Business logic, orchestrates repositories
├─────────────────────────────────────────┤
│ Repositories (app/repositories/)         │  Only layer that writes SQLAlchemy queries
├─────────────────────────────────────────┤
│ Models (app/models/) + Base (app/db/)    │  ORM entities
└─────────────────────────────────────────┘
```

Cross-cutting concerns sit outside this stack: `app/core/` (config,
logging, domain exceptions), `app/middleware/` (request context,
centralized error→HTTP translation), `app/db/` (session/connection
factories for Postgres, Redis, Qdrant).

Domain exceptions (`app/core/exceptions.py`) are the boundary contract:
services raise `NotFoundError`, `ConflictError`, etc.; routers never
catch them — `app/middleware/error_handling.py` translates every
registered exception type to the right HTTP status centrally, so that
mapping is defined once.

## Frontend structure (feature-first, App Router)

```
src/
├── app/                 Routes (App Router — folder = URL segment)
├── components/
│   ├── ui/              Design-system primitives (shadcn/ui pattern)
│   ├── layout/           App chrome (shell, nav, signature elements)
│   └── providers/        Cross-cutting context (theme, query client)
├── lib/                 Framework-agnostic utilities (cn(), etc.)
├── hooks/               Shared React hooks (empty — first feature adds one)
├── config/               Site-wide constants (nav, metadata)
└── types/                Shared TypeScript types
```

As features grow, feature-specific components/hooks/types should live
alongside their route (e.g. `app/experiments/_components/`) rather than
crowding the shared `components/` tree — "feature-first" means shared
infrastructure is the exception, not the default.

## Design language

The console UI is deliberately an instrument-panel aesthetic (near-black
`ink` background, phosphor-cyan `signal` accent, monospace data
readouts, corner-bracketed `Panel` components) rather than a generic
SaaS dashboard — see `tailwind.config.ts` for the token definitions and
`src/components/ui/panel.tsx` for the signature framing component. New
UI should extend these tokens rather than introducing ad hoc colors.

## Extension points

| Where | What plugs in later |
| --- | --- |
| `app/api/deps.py::get_current_user` | Implemented — real JWT/cookie auth (see docs/authentication.md) |
| `app/ai/provider.py::AIProvider` | Anthropic-backed implementation |
| `app/db/qdrant_client.py` | Embedding + semantic search once AI lands |
| `app/db/base_registry.py` | Import point for every new ORM model |
| `shared/openapi/` | Generated OpenAPI schema for frontend codegen |
| `infrastructure/environments/{staging,production}/` | Cloud provisioning once a target is chosen |
| `src/app/experiments`, `datasets`, `publications` | Placeholder routes reserved for those feature domains |

## Versioning

The API is versioned at the URL level (`/api/v1`, later `/api/v2`) via
`app/api/v1/router.py`, so breaking changes get a new version rather
than breaking existing consumers.
