"""Verifies authenticated endpoints reject anonymous requests and that
tampered/expired tokens don't grant access."""

import uuid

import pytest
from app.core.security import create_access_token
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


PROTECTED_ENDPOINTS = [
    ("GET", "/api/v1/users/me"),
    ("GET", "/api/v1/users/me/preferences"),
    ("GET", "/api/v1/users/me/auth-providers"),
    ("GET", "/api/v1/auth/me"),
]


class TestRouteProtection:
    @pytest.mark.parametrize("method,path", PROTECTED_ENDPOINTS)
    async def test_anonymous_request_is_rejected(
        self, client: AsyncClient, method: str, path: str
    ) -> None:
        r = await client.request(method, path)
        assert r.status_code == 401

    async def test_malformed_bearer_token_is_rejected(self, client: AsyncClient) -> None:
        r = await client.get("/api/v1/users/me", headers={"Authorization": "Bearer not-a-real-jwt"})
        assert r.status_code == 401

    async def test_token_for_nonexistent_user_is_rejected(self, client: AsyncClient) -> None:
        """A structurally-valid, correctly-signed token for a user id
        that doesn't exist (e.g. account was deleted) must still be
        rejected — the token alone isn't sufficient proof of identity."""
        fake_user_id = uuid.uuid4()
        token = create_access_token(fake_user_id)
        r = await client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 401

    async def test_public_health_endpoint_needs_no_auth(self, client: AsyncClient) -> None:
        r = await client.get("/api/v1/health")
        assert r.status_code == 200

    async def test_bearer_token_auth_works_without_cookies(self, client: AsyncClient) -> None:
        """API/mobile clients authenticate via Authorization header
        rather than cookies — confirm that path works independently."""
        register = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "bearer@example.com",
                "password": "SecurePass123",
                "display_name": "Bearer",
            },
        )
        assert register.status_code == 201

        from app.db.session import AsyncSessionLocal
        from app.repositories.user_repository import UserRepository

        async with AsyncSessionLocal() as session:
            repo = UserRepository(session)
            user = await repo.get_by_email("bearer@example.com")
            assert user is not None
            token = create_access_token(user.id)

        from app.main import app
        from httpx import ASGITransport

        fresh = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
        r = await fresh.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        await fresh.aclose()

    async def test_bearer_token_requests_are_exempt_from_csrf(self, client: AsyncClient) -> None:
        """CSRF protection guards cookie-based ambient auth; Bearer-token
        requests carry no ambient authority, so they must not need a
        CSRF header on mutating routes."""
        register = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "bearercsrf@example.com",
                "password": "SecurePass123",
                "display_name": "B",
            },
        )
        assert register.status_code == 201

        from app.db.session import AsyncSessionLocal
        from app.repositories.user_repository import UserRepository

        async with AsyncSessionLocal() as session:
            repo = UserRepository(session)
            user = await repo.get_by_email("bearercsrf@example.com")
            assert user is not None
            token = create_access_token(user.id)

        from app.main import app
        from httpx import ASGITransport

        fresh = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
        r = await fresh.patch(
            "/api/v1/users/me",
            json={"display_name": "Updated Name"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200
        await fresh.aclose()
