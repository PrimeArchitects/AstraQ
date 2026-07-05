"""Verifies every error path returns the same consistent JSON envelope
(`{"error": ..., "detail": ...}`) — validation errors, domain errors,
and raw database errors alike."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


class TestErrorEnvelopeConsistency:
    async def test_domain_error_shape(self, client: AsyncClient) -> None:
        """A domain error (e.g. wrong login) uses the {error, detail} shape."""
        r = await client.post(
            "/api/v1/auth/login", json={"email": "nobody@example.com", "password": "WrongPass123"}
        )
        assert r.status_code == 401
        body = r.json()
        assert set(body.keys()) == {"error", "detail"}
        assert body["error"] == "UnauthorizedError"

    async def test_pydantic_validation_error_shape_matches_domain_errors(
        self, client: AsyncClient
    ) -> None:
        """FastAPI's default validation-error body is reshaped to match
        every other error response, rather than leaking its own
        differently-shaped {"detail": [...]} format."""
        r = await client.post(
            "/api/v1/auth/register",
            json={"email": "not-an-email", "password": "short", "display_name": ""},
        )
        assert r.status_code == 422
        body = r.json()
        assert body["error"] == "ValidationError"
        assert isinstance(body["detail"], str)
        assert "errors" in body  # full Pydantic error list still available for debugging

    async def test_database_integrity_error_becomes_409_not_500(self) -> None:
        """A unique-constraint violation that reaches the DB directly
        (bypassing a service-level pre-check — e.g. a race between two
        concurrent requests) must surface as a clean 409, not a raw 500
        with leaked DB internals. Tests the handler directly since
        reliably forcing a real race through the HTTP layer would be
        flaky."""
        from unittest.mock import MagicMock

        from app.middleware.error_handling import integrity_error_handler
        from sqlalchemy.exc import IntegrityError

        fake_error = IntegrityError("INSERT INTO users ...", {}, Exception("duplicate key value"))
        response = await integrity_error_handler(MagicMock(), fake_error)

        assert response.status_code == 409
        body = response.body.decode()
        assert "ConflictError" in body
        # The raw DB error text must never reach the client.
        assert "duplicate key value" not in body
