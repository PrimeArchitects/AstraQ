# shared/

Artifacts that both `frontend/` and `backend/` need to agree on, so the
contract lives in one place instead of being duplicated and drifting.

- **openapi/** — the backend publishes its OpenAPI schema here (via
  `scripts/export-openapi.sh`, added when the first real API contract
  exists). The frontend can codegen a typed client from it instead of
  hand-writing fetch wrappers.

Nothing is generated yet in this foundation phase — this directory exists
so the wiring has a home when the first real endpoints ship.
