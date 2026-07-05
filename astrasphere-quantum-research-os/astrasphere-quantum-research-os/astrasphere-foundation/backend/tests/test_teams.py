"""Integration tests for placeholder team-workspace CRUD and membership."""

import pytest
from httpx import AsyncClient

from tests.conftest import new_client, register_user

pytestmark = pytest.mark.anyio


class TestTeams:
    async def test_create_workspace_makes_creator_owner_member(self, client: AsyncClient) -> None:
        await register_user(client)
        r = await client.post("/api/v1/teams", json={"name": "Quantum Lab"})
        assert r.status_code == 201, r.text
        workspace = r.json()

        r = await client.get(f"/api/v1/teams/{workspace['id']}/members")
        assert r.status_code == 200
        members = r.json()
        assert len(members) == 1
        assert members[0]["role"] == "owner"

    async def test_non_member_cannot_access_workspace(self, client: AsyncClient) -> None:
        await register_user(client, "teamowner@example.com")
        workspace = (await client.post("/api/v1/teams", json={"name": "Private Lab"})).json()

        other = new_client()
        await register_user(other, "outsider@example.com")
        r = await other.get(f"/api/v1/teams/{workspace['id']}")
        assert r.status_code == 403
        await other.aclose()

    async def test_owner_can_update_and_delete_workspace(self, client: AsyncClient) -> None:
        await register_user(client)
        workspace = (await client.post("/api/v1/teams", json={"name": "Old name"})).json()

        r = await client.patch(f"/api/v1/teams/{workspace['id']}", json={"name": "New name"})
        assert r.status_code == 200
        assert r.json()["name"] == "New name"

        r = await client.delete(f"/api/v1/teams/{workspace['id']}")
        assert r.status_code == 204
