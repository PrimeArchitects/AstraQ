"""Integration tests for registration, login, session lifecycle, and
password/email flows — run against a real Postgres + Redis (see
conftest.py), not mocks."""

import pytest
from app.core.security import create_email_verification_token, create_password_reset_token
from app.db.session import AsyncSessionLocal
from app.repositories.user_repository import UserRepository
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def _register(client: AsyncClient, email: str = "researcher@example.com") -> None:
    r = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123", "display_name": "Dr. Test"},
    )
    assert r.status_code == 201, r.text


class TestRegistration:
    async def test_register_returns_user_and_sets_cookies(self, client: AsyncClient) -> None:
        r = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "new@example.com",
                "password": "SecurePass123",
                "display_name": "New User",
            },
        )
        assert r.status_code == 201
        body = r.json()
        assert body["email"] == "new@example.com"
        assert body["email_verified"] is False
        assert "astrasphere_access" in r.cookies
        assert "astrasphere_refresh" in r.cookies
        assert "astrasphere_csrf" in r.cookies

    async def test_register_duplicate_email_conflicts(self, client: AsyncClient) -> None:
        await _register(client, "dup@example.com")
        r = await client.post(
            "/api/v1/auth/register",
            json={"email": "dup@example.com", "password": "SecurePass123", "display_name": "Dup"},
        )
        assert r.status_code == 409

    async def test_register_email_is_case_insensitive_for_dupes(self, client: AsyncClient) -> None:
        await _register(client, "case@example.com")
        r = await client.post(
            "/api/v1/auth/register",
            json={"email": "CASE@EXAMPLE.COM", "password": "SecurePass123", "display_name": "Dup"},
        )
        assert r.status_code == 409

    async def test_register_creates_preferences_and_password_provider(
        self, client: AsyncClient
    ) -> None:
        await _register(client, "prefs@example.com")
        async with AsyncSessionLocal() as session:
            repo = UserRepository(session)
            user = await repo.get_by_email("prefs@example.com")
            assert user is not None
            prefs = await repo.get_preferences(user.id)
            assert prefs is not None
            assert prefs.theme == "dark"
            providers = await repo.list_auth_providers(user.id)
            assert any(p.provider == "password" for p in providers)


class TestLogin:
    async def test_login_with_correct_credentials(self, client: AsyncClient) -> None:
        await _register(client, "login@example.com")
        fresh = AsyncClient(transport=client._transport, base_url="http://test")  # type: ignore[attr-defined]
        r = await fresh.post(
            "/api/v1/auth/login", json={"email": "login@example.com", "password": "SecurePass123"}
        )
        assert r.status_code == 200
        await fresh.aclose()

    async def test_login_with_wrong_password(self, client: AsyncClient) -> None:
        await _register(client, "wrongpw@example.com")
        r = await client.post(
            "/api/v1/auth/login", json={"email": "wrongpw@example.com", "password": "WrongPass123"}
        )
        assert r.status_code == 401

    async def test_login_with_nonexistent_email(self, client: AsyncClient) -> None:
        r = await client.post(
            "/api/v1/auth/login", json={"email": "nobody@example.com", "password": "SecurePass123"}
        )
        assert r.status_code == 401

    async def test_login_error_message_does_not_distinguish_missing_vs_wrong(
        self, client: AsyncClient
    ) -> None:
        """Both failure modes must return an identical message, or the
        API becomes an account-existence oracle."""
        await _register(client, "exists@example.com")
        r_wrong_pw = await client.post(
            "/api/v1/auth/login", json={"email": "exists@example.com", "password": "WrongPass123"}
        )
        r_no_account = await client.post(
            "/api/v1/auth/login", json={"email": "nobody@example.com", "password": "WrongPass123"}
        )
        assert r_wrong_pw.json()["detail"] == r_no_account.json()["detail"]


class TestSessionLifecycle:
    async def test_refresh_issues_new_tokens_and_rotates(self, client: AsyncClient) -> None:
        await _register(client, "refresh@example.com")
        old_refresh = client.cookies.get("astrasphere_refresh")

        r = await client.post("/api/v1/auth/refresh")
        assert r.status_code == 200
        new_refresh = client.cookies.get("astrasphere_refresh")
        assert new_refresh != old_refresh

    async def test_reusing_a_rotated_refresh_token_fails(self, client: AsyncClient) -> None:
        await _register(client, "reuse@example.com")
        old_refresh = client.cookies.get("astrasphere_refresh")

        await client.post("/api/v1/auth/refresh")  # rotates; old_refresh is now revoked

        client.cookies.set("astrasphere_refresh", old_refresh)
        r = await client.post("/api/v1/auth/refresh")
        assert r.status_code == 401

    async def test_logout_requires_csrf_header(self, client: AsyncClient) -> None:
        await _register(client, "logoutcsrf@example.com")
        r = await client.post("/api/v1/auth/logout")
        assert r.status_code == 403

    async def test_logout_with_csrf_revokes_session(self, client: AsyncClient) -> None:
        await _register(client, "logout@example.com")
        csrf = client.cookies.get("astrasphere_csrf")

        r = await client.post("/api/v1/auth/logout", headers={"X-CSRF-Token": csrf})
        assert r.status_code == 200

        r2 = await client.get("/api/v1/users/me")
        assert r2.status_code == 401


class TestEmailVerification:
    async def test_verify_with_valid_token(self, client: AsyncClient) -> None:
        await _register(client, "verify@example.com")
        async with AsyncSessionLocal() as session:
            repo = UserRepository(session)
            user = await repo.get_by_email("verify@example.com")
            assert user is not None
            token = create_email_verification_token(user.id, user.email)

        r = await client.get(f"/api/v1/auth/verify-email?token={token}")
        assert r.status_code == 200

        r2 = await client.get("/api/v1/auth/me")
        assert r2.json()["email_verified"] is True

    async def test_verify_with_garbage_token_fails_clearly(self, client: AsyncClient) -> None:
        r = await client.get("/api/v1/auth/verify-email?token=not-a-real-token")
        assert r.status_code == 422
        assert "invalid or has expired" in r.json()["detail"]


class TestPasswordReset:
    async def test_forgot_password_always_returns_generic_success(
        self, client: AsyncClient
    ) -> None:
        """Whether or not the email is registered, the response must be
        identical — otherwise this endpoint leaks account existence."""
        r_real = await client.post(
            "/api/v1/auth/forgot-password", json={"email": "ghost@example.com"}
        )
        r_fake = await client.post(
            "/api/v1/auth/forgot-password", json={"email": "definitely-not-registered@example.com"}
        )
        assert r_real.status_code == r_fake.status_code == 200
        assert r_real.json() == r_fake.json()

    async def test_reset_password_with_valid_token(self, client: AsyncClient) -> None:
        await _register(client, "reset@example.com")
        async with AsyncSessionLocal() as session:
            repo = UserRepository(session)
            user = await repo.get_by_email("reset@example.com")
            assert user is not None
            from app.core.security import fingerprint

            token = create_password_reset_token(user.id, fingerprint(user.hashed_password))  # type: ignore[arg-type]

        r = await client.post(
            "/api/v1/auth/reset-password", json={"token": token, "new_password": "BrandNewPass123"}
        )
        assert r.status_code == 200

        fresh = AsyncClient(transport=client._transport, base_url="http://test")  # type: ignore[attr-defined]
        r2 = await fresh.post(
            "/api/v1/auth/login", json={"email": "reset@example.com", "password": "BrandNewPass123"}
        )
        assert r2.status_code == 200
        await fresh.aclose()

    async def test_reset_token_cannot_be_reused(self, client: AsyncClient) -> None:
        await _register(client, "reuse-reset@example.com")
        async with AsyncSessionLocal() as session:
            repo = UserRepository(session)
            user = await repo.get_by_email("reuse-reset@example.com")
            assert user is not None
            from app.core.security import fingerprint

            token = create_password_reset_token(user.id, fingerprint(user.hashed_password))  # type: ignore[arg-type]

        r1 = await client.post(
            "/api/v1/auth/reset-password", json={"token": token, "new_password": "FirstNewPass123"}
        )
        assert r1.status_code == 200

        r2 = await client.post(
            "/api/v1/auth/reset-password", json={"token": token, "new_password": "SecondNewPass123"}
        )
        assert r2.status_code == 422

    async def test_password_reset_revokes_existing_sessions(self, client: AsyncClient) -> None:
        await _register(client, "revoke@example.com")
        # This client's cookies are for the pre-reset session.
        async with AsyncSessionLocal() as session:
            repo = UserRepository(session)
            user = await repo.get_by_email("revoke@example.com")
            assert user is not None
            from app.core.security import fingerprint

            token = create_password_reset_token(user.id, fingerprint(user.hashed_password))  # type: ignore[arg-type]

        await client.post(
            "/api/v1/auth/reset-password",
            json={"token": token, "new_password": "AfterResetPass123"},
        )

        # The old session's refresh token must no longer work.
        r = await client.post("/api/v1/auth/refresh")
        assert r.status_code == 401
