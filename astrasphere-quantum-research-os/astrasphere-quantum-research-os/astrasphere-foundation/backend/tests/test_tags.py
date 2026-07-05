"""Integration tests for tag CRUD."""

import pytest
from httpx import AsyncClient

from tests.conftest import register_user

pytestmark = pytest.mark.anyio


class TestTags:
    async def test_create_and_list_tag(self, client: AsyncClient) -> None:
        await register_user(client)
        r = await client.post("/api/v1/tags", json={"name": "entanglement", "color": "#4CE0D2"})
        assert r.status_code == 201, r.text

        r = await client.get("/api/v1/tags")
        assert r.status_code == 200
        assert len(r.json()) == 1

    async def test_duplicate_tag_name_conflicts(self, client: AsyncClient) -> None:
        await register_user(client)
        await client.post("/api/v1/tags", json={"name": "qubits"})
        r = await client.post("/api/v1/tags", json={"name": "qubits"})
        assert r.status_code == 409

    async def test_update_and_delete_tag(self, client: AsyncClient) -> None:
        await register_user(client)
        tag = (await client.post("/api/v1/tags", json={"name": "old"})).json()

        r = await client.patch(f"/api/v1/tags/{tag['id']}", json={"name": "new"})
        assert r.status_code == 200
        assert r.json()["name"] == "new"

        r = await client.delete(f"/api/v1/tags/{tag['id']}")
        assert r.status_code == 204
