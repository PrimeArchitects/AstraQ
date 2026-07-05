"""Integration tests for the audit trail: verifies that mutating
endpoints across other domains actually write activity_log rows."""

import pytest
from httpx import AsyncClient

from tests.conftest import register_user

pytestmark = pytest.mark.anyio


class TestActivityLogs:
    async def test_creating_a_folder_is_logged(self, client: AsyncClient) -> None:
        await register_user(client)
        await client.post("/api/v1/folders", json={"name": "Logged folder"})

        r = await client.get("/api/v1/activity-logs")
        assert r.status_code == 200
        body = r.json()
        assert body["total"] >= 1
        actions = [log["action"] for log in body["items"]]
        resource_types = [log["resource_type"] for log in body["items"]]
        assert "create" in actions
        assert "folder" in resource_types

    async def test_multiple_actions_accumulate(self, client: AsyncClient) -> None:
        await register_user(client)
        tag = (await client.post("/api/v1/tags", json={"name": "logged"})).json()
        await client.patch(f"/api/v1/tags/{tag['id']}", json={"name": "renamed"})
        await client.delete(f"/api/v1/tags/{tag['id']}")

        r = await client.get("/api/v1/activity-logs", params={"page_size": 50})
        resource_types = [log["resource_type"] for log in r.json()["items"]]
        assert resource_types.count("tag") >= 2  # create + delete are logged

    async def test_activity_logs_are_paginated(self, client: AsyncClient) -> None:
        await register_user(client)
        for i in range(3):
            await client.post("/api/v1/folders", json={"name": f"Folder {i}"})

        r = await client.get("/api/v1/activity-logs", params={"page_size": 2})
        body = r.json()
        assert len(body["items"]) == 2
        assert body["total"] >= 3
