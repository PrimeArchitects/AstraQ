# Contributing

## Branching

- `main` is always deployable.
- Branch per change: `feat/<short-description>`, `fix/<short-description>`,
  `chore/<short-description>`, `docs/<short-description>`.
- Open a PR into `main`. CI (`.github/workflows/ci.yml`) must pass
  before merge.

## Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(backend): add experiment repository
fix(frontend): correct panel border radius on mobile
docs: update installation prerequisites
chore(deps): bump fastapi to 0.115.x
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
Scope (optional): `backend`, `frontend`, `infra`, `docs`.

## Before opening a PR

```bash
make lint     # backend ruff + frontend eslint
make format   # backend black + frontend prettier
make test     # backend pytest + frontend vitest
```

Or let the pre-commit hooks (Husky for frontend, pre-commit for
backend) catch formatting issues automatically on `git commit`.

## Code review expectations

- **Layering** — backend PRs should respect router → service →
  repository (see `docs/architecture.md`); flag it in review if a
  router imports SQLAlchemy directly, or a service imports FastAPI.
- **Types** — no `any` in TypeScript, no untyped functions in Python
  (`mypy --strict` runs in CI). Justify any `# type: ignore` /
  `@ts-expect-error` with a comment.
- **Tests** — new endpoints/services get at least one test. New UI
  components with logic (not pure presentation) get a test if the
  logic branches.
- **Design tokens** — new UI uses existing Tailwind tokens
  (`tailwind.config.ts`) rather than introducing new hex values inline.
- **Migrations** — schema changes ship with an Alembic migration in
  the same PR as the model change, not as a follow-up.

## Reporting issues

Include: what you expected, what happened, steps to reproduce, and
`docker compose ps` / relevant log output if it's a runtime issue.
