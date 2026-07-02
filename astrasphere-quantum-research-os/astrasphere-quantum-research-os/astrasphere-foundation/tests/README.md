# tests/

Cross-service integration tests that exercise the frontend and backend
together (or the backend against real Postgres/Redis/Qdrant containers).

Unit tests live next to the code they test: `backend/tests/` for the
API, `frontend/src/**/*.test.tsx` for components. This directory is for
tests that don't belong to a single service — e.g. "does the frontend's
API client actually parse what the backend returns."

Empty in the foundation phase; the health-check integration test below
is the first entry once routers exist beyond `/health`.
