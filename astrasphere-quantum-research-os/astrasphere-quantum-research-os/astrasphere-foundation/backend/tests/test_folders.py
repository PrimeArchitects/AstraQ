"""Integration tests for folder CRUD, nesting, and ownership isolation."""

import pytest
from httpx import AsyncClient

from tests.conftest import new_client, register_user

pytestmark = pytest.mark.anyio


class TestFolders:
    async def test_create_and_list_folder(self, client: AsyncClient) -> None:
        await register_user(client)
        r = await client.post("/api/v1/folders", json={"name": "Quantum Computing"})
        assert r.status_code == 201, r.text
        assert r.json()["name"] == "Quantum Computing"

        r = await client.get("/api/v1/folders")
        assert r.status_code == 200
        assert len(r.json()) == 1

    async def test_duplicate_name_at_same_level_conflicts(self, client: AsyncClient) -> None:
        await register_user(client)
        await client.post("/api/v1/folders", json={"name": "Dup"})
        r = await client.post("/api/v1/folders", json={"name": "Dup"})
        assert r.status_code == 409

    async def test_nested_folder(self, client: AsyncClient) -> None:
        await register_user(client)
        parent = (await client.post("/api/v1/folders", json={"name": "Parent"})).json()
        r = await client.post("/api/v1/folders", json={"name": "Child", "parent_id": parent["id"]})
        assert r.status_code == 201
        assert r.json()["parent_id"] == parent["id"]

    async def test_folder_cannot_be_its_own_parent(self, client: AsyncClient) -> None:
        await register_user(client)
        folder = (await client.post("/api/v1/folders", json={"name": "Self"})).json()
        r = await client.patch(f"/api/v1/folders/{folder['id']}", json={"parent_id": folder["id"]})
        assert r.status_code == 422

    async def test_update_and_delete_folder(self, client: AsyncClient) -> None:
        await register_user(client)
        folder = (await client.post("/api/v1/folders", json={"name": "Old"})).json()

        r = await client.patch(f"/api/v1/folders/{folder['id']}", json={"name": "New"})
        assert r.status_code == 200
        assert r.json()["name"] == "New"

        r = await client.delete(f"/api/v1/folders/{folder['id']}")
        assert r.status_code == 204

        r = await client.get(f"/api/v1/folders/{folder['id']}")
        assert r.status_code == 404

    async def test_folders_are_isolated_per_user(self, client: AsyncClient) -> None:
        await register_user(client, "owner@example.com")
        folder = (await client.post("/api/v1/folders", json={"name": "Private"})).json()

        other_client = new_client()
        await register_user(other_client, "other@example.com")
        r = await other_client.get(f"/api/v1/folders/{folder['id']}")
        assert r.status_code == 404
        await other_client.aclose()

    async def test_unauthenticated_request_rejected(self, client: AsyncClient) -> None:
        r = await client.get("/api/v1/folders")
        assert r.status_code == 401
