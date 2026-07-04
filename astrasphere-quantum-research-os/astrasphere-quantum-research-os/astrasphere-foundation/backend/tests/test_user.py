"""Integration tests for profile management, preferences, and account deletion."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def _register(client: AsyncClient, email: str = "profile@example.com") -> None:
    r = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123", "display_name": "Dr. Test"},
    )
    assert r.status_code == 201


def _csrf_headers(client: AsyncClient) -> dict[str, str]:
    return {"X-CSRF-Token": client.cookies.get("astrasphere_csrf")}


class TestProfile:
    async def test_get_profile_shape(self, client: AsyncClient) -> None:
        await _register(client, "shape@example.com")
        r = await client.get("/api/v1/users/me")
        body = r.json()
        assert set(body.keys()) >= {
            "id",
            "email",
            "display_name",
            "bio",
            "institution",
            "research_interests",
            "timezone",
            "email_verified",
            "created_at",
        }

    async def test_update_profile_requires_csrf(self, client: AsyncClient) -> None:
        await _register(client, "nocsrf@example.com")
        r = await client.patch("/api/v1/users/me", json={"display_name": "New Name"})
        assert r.status_code == 403

    async def test_update_profile_fields(self, client: AsyncClient) -> None:
        await _register(client, "update@example.com")
        r = await client.patch(
            "/api/v1/users/me",
            json={
                "display_name": "Dr. Updated",
                "institution": "AstraSphere University",
                "research_interests": ["error correction", "photonics"],
                "bio": "Quantum error correction researcher.",
            },
            headers=_csrf_headers(client),
        )
        assert r.status_code == 200
        body = r.json()
        assert body["display_name"] == "Dr. Updated"
        assert body["institution"] == "AstraSphere University"
        assert body["research_interests"] == ["error correction", "photonics"]

    async def test_partial_update_leaves_other_fields_untouched(self, client: AsyncClient) -> None:
        await _register(client, "partial@example.com")
        await client.patch(
            "/api/v1/users/me", json={"institution": "Original U"}, headers=_csrf_headers(client)
        )
        r = await client.patch(
            "/api/v1/users/me", json={"bio": "Just a bio update."}, headers=_csrf_headers(client)
        )
        assert r.status_code == 200
        assert r.json()["institution"] == "Original U"
        assert r.json()["bio"] == "Just a bio update."


class TestPreferences:
    async def test_default_preferences(self, client: AsyncClient) -> None:
        await _register(client, "defaultprefs@example.com")
        r = await client.get("/api/v1/users/me/preferences")
        assert r.status_code == 200
        body = r.json()
        assert body["theme"] == "dark"
        assert body["notify_citations"] is True
        assert body["notify_weekly_digest"] is False

    async def test_update_theme_preference(self, client: AsyncClient) -> None:
        await _register(client, "theme@example.com")
        r = await client.patch(
            "/api/v1/users/me/preferences", json={"theme": "light"}, headers=_csrf_headers(client)
        )
        assert r.status_code == 200
        assert r.json()["theme"] == "light"

    async def test_invalid_theme_rejected(self, client: AsyncClient) -> None:
        await _register(client, "badtheme@example.com")
        r = await client.patch(
            "/api/v1/users/me/preferences",
            json={"theme": "neon"},
            headers=_csrf_headers(client),
        )
        assert r.status_code == 422


class TestAuthProviders:
    async def test_password_provider_listed_after_registration(self, client: AsyncClient) -> None:
        await _register(client, "providers@example.com")
        r = await client.get("/api/v1/users/me/auth-providers")
        assert r.status_code == 200
        providers = [p["provider"] for p in r.json()]
        assert "password" in providers


class TestChangePassword:
    async def test_change_password_with_wrong_current_password(self, client: AsyncClient) -> None:
        await _register(client, "changepw@example.com")
        r = await client.post(
            "/api/v1/auth/change-password",
            json={"current_password": "WrongOldPass1", "new_password": "BrandNewPass123"},
            headers=_csrf_headers(client),
        )
        assert r.status_code == 401

    async def test_change_password_success_revokes_session(self, client: AsyncClient) -> None:
        await _register(client, "changepwok@example.com")
        r = await client.post(
            "/api/v1/auth/change-password",
            json={"current_password": "SecurePass123", "new_password": "BrandNewPass123"},
            headers=_csrf_headers(client),
        )
        assert r.status_code == 200

        r2 = await client.get("/api/v1/users/me")
        assert r2.status_code == 401


class TestAccountDeletion:
    async def test_delete_requires_confirmation(self, client: AsyncClient) -> None:
        await _register(client, "delnoconfirm@example.com")
        r = await client.request(
            "DELETE",
            "/api/v1/users/me",
            json={"password": "SecurePass123", "confirm": False},
            headers=_csrf_headers(client),
        )
        assert r.status_code == 422

    async def test_delete_requires_correct_password(self, client: AsyncClient) -> None:
        await _register(client, "delwrongpw@example.com")
        r = await client.request(
            "DELETE",
            "/api/v1/users/me",
            json={"password": "WrongPassword1", "confirm": True},
            headers=_csrf_headers(client),
        )
        assert r.status_code == 401

    async def test_delete_account_success(self, client: AsyncClient) -> None:
        await _register(client, "deleteme@example.com")
        r = await client.request(
            "DELETE",
            "/api/v1/users/me",
            json={"password": "SecurePass123", "confirm": True},
            headers=_csrf_headers(client),
        )
        assert r.status_code == 204

        fresh = AsyncClient(transport=client._transport, base_url="http://test")  # type: ignore[attr-defined]
        r2 = await fresh.post(
            "/api/v1/auth/login",
            json={"email": "deleteme@example.com", "password": "SecurePass123"},
        )
        assert r2.status_code == 401
        await fresh.aclose()
