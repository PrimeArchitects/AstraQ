"""Integration tests for research paper CRUD, pagination, filtering,
sorting, tag linking, metadata, and soft delete."""

import pytest
from httpx import AsyncClient

from tests.conftest import new_client, register_user

pytestmark = pytest.mark.anyio


class TestPapers:
    async def test_create_and_get_paper(self, client: AsyncClient) -> None:
        await register_user(client)
        r = await client.post(
            "/api/v1/papers",
            json={"title": "Quantum Error Correction", "authors": ["A. Kitaev"], "year": 2003},
        )
        assert r.status_code == 201, r.text
        body = r.json()
        assert body["title"] == "Quantum Error Correction"
        assert body["status"] == "new"
        assert body["progress"] == 0

        r = await client.get(f"/api/v1/papers/{body['id']}")
        assert r.status_code == 200

    async def test_pagination_envelope(self, client: AsyncClient) -> None:
        await register_user(client)
        for i in range(5):
            await client.post("/api/v1/papers", json={"title": f"Paper {i}"})

        r = await client.get("/api/v1/papers", params={"page": 1, "page_size": 2})
        assert r.status_code == 200
        body = r.json()
        assert len(body["items"]) == 2
        assert body["total"] == 5
        assert body["total_pages"] == 3
        assert body["page"] == 1

    async def test_filter_by_status(self, client: AsyncClient) -> None:
        await register_user(client)
        await client.post("/api/v1/papers", json={"title": "New paper"})
        reading = (await client.post("/api/v1/papers", json={"title": "Reading paper"})).json()
        await client.patch(f"/api/v1/papers/{reading['id']}", json={"status": "reading"})

        r = await client.get("/api/v1/papers", params={"status": "reading"})
        assert r.status_code == 200
        body = r.json()
        assert body["total"] == 1
        assert body["items"][0]["title"] == "Reading paper"

    async def test_search_by_title(self, client: AsyncClient) -> None:
        await register_user(client)
        await client.post("/api/v1/papers", json={"title": "Topological Qubits"})
        await client.post("/api/v1/papers", json={"title": "Neural Networks"})

        r = await client.get("/api/v1/papers", params={"search": "qubit"})
        body = r.json()
        assert body["total"] == 1
        assert "Qubits" in body["items"][0]["title"]

    async def test_sort_by_title_ascending(self, client: AsyncClient) -> None:
        await register_user(client)
        await client.post("/api/v1/papers", json={"title": "Zebra"})
        await client.post("/api/v1/papers", json={"title": "Apple"})

        r = await client.get("/api/v1/papers", params={"sort_by": "title", "sort_order": "asc"})
        titles = [item["title"] for item in r.json()["items"]]
        assert titles == ["Apple", "Zebra"]

    async def test_tag_linking(self, client: AsyncClient) -> None:
        await register_user(client)
        tag = (await client.post("/api/v1/tags", json={"name": "topology"})).json()
        r = await client.post(
            "/api/v1/papers", json={"title": "Tagged paper", "tag_ids": [tag["id"]]}
        )
        assert r.status_code == 201
        assert r.json()["tags"][0]["name"] == "topology"

    async def test_invalid_tag_id_rejected(self, client: AsyncClient) -> None:
        await register_user(client)
        r = await client.post(
            "/api/v1/papers",
            json={"title": "Bad tag paper", "tag_ids": ["00000000-0000-0000-0000-000000000000"]},
        )
        assert r.status_code == 422

    async def test_metadata_upsert(self, client: AsyncClient) -> None:
        await register_user(client)
        paper = (await client.post("/api/v1/papers", json={"title": "DOI paper"})).json()

        r = await client.put(
            f"/api/v1/papers/{paper['id']}/metadata",
            json={"doi": "10.1234/abcd", "citation_count": 42},
        )
        assert r.status_code == 200
        assert r.json()["metadata_record"]["doi"] == "10.1234/abcd"
        assert r.json()["metadata_record"]["citation_count"] == 42

    async def test_soft_delete_hides_paper(self, client: AsyncClient) -> None:
        await register_user(client)
        paper = (await client.post("/api/v1/papers", json={"title": "To delete"})).json()

        r = await client.delete(f"/api/v1/papers/{paper['id']}")
        assert r.status_code == 204

        r = await client.get(f"/api/v1/papers/{paper['id']}")
        assert r.status_code == 404

        r = await client.get("/api/v1/papers")
        assert r.json()["total"] == 0

    async def test_papers_isolated_per_owner(self, client: AsyncClient) -> None:
        await register_user(client, "owner@example.com")
        paper = (await client.post("/api/v1/papers", json={"title": "Private paper"})).json()

        other_client = new_client()
        await register_user(other_client, "other@example.com")
        r = await other_client.get(f"/api/v1/papers/{paper['id']}")
        assert r.status_code == 404
        await other_client.aclose()
