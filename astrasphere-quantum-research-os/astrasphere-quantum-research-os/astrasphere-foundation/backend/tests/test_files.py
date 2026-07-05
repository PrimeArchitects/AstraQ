"""Integration tests for file-metadata CRUD (no actual upload handling)."""

import pytest
from httpx import AsyncClient

from tests.conftest import register_user

pytestmark = pytest.mark.anyio


class TestFiles:
    async def test_register_file_metadata(self, client: AsyncClient) -> None:
        await register_user(client)
        r = await client.post(
            "/api/v1/files",
            json={
                "filename": "paper.pdf",
                "file_size": 204800,
                "storage_path": "uploads/2026/07/paper.pdf",
                "checksum": "abc123",
                "content_type": "application/pdf",
            },
        )
        assert r.status_code == 201, r.text
        assert r.json()["processing_status"] == "pending"

    async def test_file_linked_to_paper(self, client: AsyncClient) -> None:
        await register_user(client)
        paper = (await client.post("/api/v1/papers", json={"title": "Has file"})).json()
        r = await client.post(
            "/api/v1/files",
            json={
                "paper_id": paper["id"],
                "filename": "linked.pdf",
                "file_size": 1024,
                "storage_path": "uploads/linked.pdf",
                "checksum": "def456",
            },
        )
        assert r.status_code == 201
        assert r.json()["paper_id"] == paper["id"]

    async def test_file_for_missing_paper_404s(self, client: AsyncClient) -> None:
        await register_user(client)
        r = await client.post(
            "/api/v1/files",
            json={
                "paper_id": "00000000-0000-0000-0000-000000000000",
                "filename": "orphan.pdf",
                "file_size": 1,
                "storage_path": "x",
                "checksum": "x",
            },
        )
        assert r.status_code == 404

    async def test_update_processing_status_and_delete(self, client: AsyncClient) -> None:
        await register_user(client)
        file = (
            await client.post(
                "/api/v1/files",
                json={
                    "filename": "status.pdf",
                    "file_size": 1,
                    "storage_path": "x",
                    "checksum": "x",
                },
            )
        ).json()

        r = await client.patch(
            f"/api/v1/files/{file['id']}", json={"processing_status": "completed"}
        )
        assert r.status_code == 200
        assert r.json()["processing_status"] == "completed"

        r = await client.delete(f"/api/v1/files/{file['id']}")
        assert r.status_code == 204

        r = await client.get(f"/api/v1/files/{file['id']}")
        assert r.status_code == 404

    async def test_list_files_paginated(self, client: AsyncClient) -> None:
        await register_user(client)
        for i in range(3):
            await client.post(
                "/api/v1/files",
                json={
                    "filename": f"file{i}.pdf",
                    "file_size": 1,
                    "storage_path": f"x{i}",
                    "checksum": f"x{i}",
                },
            )
        r = await client.get("/api/v1/files", params={"page_size": 2})
        assert r.status_code == 200
        body = r.json()
        assert body["total"] == 3
        assert len(body["items"]) == 2
