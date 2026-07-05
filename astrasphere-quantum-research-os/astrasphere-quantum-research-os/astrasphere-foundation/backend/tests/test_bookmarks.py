"""Integration tests for bookmark CRUD and constraints."""

import pytest
from httpx import AsyncClient

from tests.conftest import register_user

pytestmark = pytest.mark.anyio


class TestBookmarks:
    async def test_bookmark_a_paper(self, client: AsyncClient) -> None:
        await register_user(client)
        paper = (await client.post("/api/v1/papers", json={"title": "Bookmarked"})).json()

        r = await client.post(
            "/api/v1/bookmarks", json={"paper_id": paper["id"], "note": "Read later"}
        )
        assert r.status_code == 201, r.text
        assert r.json()["note"] == "Read later"

        r = await client.get("/api/v1/bookmarks")
        assert r.status_code == 200
        assert r.json()["total"] == 1

    async def test_duplicate_bookmark_conflicts(self, client: AsyncClient) -> None:
        await register_user(client)
        paper = (await client.post("/api/v1/papers", json={"title": "Dup bookmark"})).json()
        await client.post("/api/v1/bookmarks", json={"paper_id": paper["id"]})

        r = await client.post("/api/v1/bookmarks", json={"paper_id": paper["id"]})
        assert r.status_code == 409

    async def test_bookmark_nonexistent_paper_404s(self, client: AsyncClient) -> None:
        await register_user(client)
        r = await client.post(
            "/api/v1/bookmarks", json={"paper_id": "00000000-0000-0000-0000-000000000000"}
        )
        assert r.status_code == 404

    async def test_update_and_delete_bookmark(self, client: AsyncClient) -> None:
        await register_user(client)
        paper = (await client.post("/api/v1/papers", json={"title": "Editable bookmark"})).json()
        bookmark = (await client.post("/api/v1/bookmarks", json={"paper_id": paper["id"]})).json()

        r = await client.patch(f"/api/v1/bookmarks/{bookmark['id']}", json={"note": "Updated"})
        assert r.status_code == 200
        assert r.json()["note"] == "Updated"

        r = await client.delete(f"/api/v1/bookmarks/{bookmark['id']}")
        assert r.status_code == 204
