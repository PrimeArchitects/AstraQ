"""Integration tests for notifications.

Notifications aren't created by any endpoint in this step (no delivery
producer exists yet), so tests insert rows directly via the ORM to
exercise the read/mark-read endpoints.
"""

import pytest
from app.db.session import AsyncSessionLocal
from app.models.notification import Notification
from app.repositories.user_repository import UserRepository
from httpx import AsyncClient

from tests.conftest import register_user

pytestmark = pytest.mark.anyio


async def _seed_notification(email: str, title: str = "New citation") -> None:
    async with AsyncSessionLocal() as session:
        user = await UserRepository(session).get_by_email(email)
        assert user is not None
        session.add(Notification(user_id=user.id, type="citation", title=title))
        await session.commit()


class TestNotifications:
    async def test_list_and_unread_count(self, client: AsyncClient) -> None:
        await register_user(client, "notif@example.com")
        await _seed_notification("notif@example.com")

        r = await client.get("/api/v1/notifications")
        assert r.status_code == 200
        assert r.json()["total"] == 1

        r = await client.get("/api/v1/notifications/unread-count")
        assert r.status_code == 200
        assert r.json()["updated"] == 1

    async def test_mark_single_read(self, client: AsyncClient) -> None:
        await register_user(client, "notif2@example.com")
        await _seed_notification("notif2@example.com")

        notifications = (await client.get("/api/v1/notifications")).json()["items"]
        notification_id = notifications[0]["id"]

        r = await client.post(f"/api/v1/notifications/{notification_id}/read")
        assert r.status_code == 200
        assert r.json()["read_at"] is not None

    async def test_mark_all_read(self, client: AsyncClient) -> None:
        await register_user(client, "notif3@example.com")
        await _seed_notification("notif3@example.com", "First")
        await _seed_notification("notif3@example.com", "Second")

        r = await client.post("/api/v1/notifications/read-all")
        assert r.status_code == 200
        assert r.json()["updated"] == 2

        r = await client.get("/api/v1/notifications/unread-count")
        assert r.json()["updated"] == 0
