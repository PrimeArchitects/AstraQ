"""Integration tests for placeholder AI job submission (no execution)."""

import pytest
from httpx import AsyncClient

from tests.conftest import new_client, register_user

pytestmark = pytest.mark.anyio


class TestAIJobs:
    async def test_submit_job_stays_queued(self, client: AsyncClient) -> None:
        await register_user(client)
        r = await client.post(
            "/api/v1/ai-jobs",
            json={"job_type": "summarize_paper", "payload": {"paper_id": "abc"}},
        )
        assert r.status_code == 201, r.text
        body = r.json()
        assert body["status"] == "queued"
        assert body["result"] is None

    async def test_list_and_get_job(self, client: AsyncClient) -> None:
        await register_user(client)
        job = (
            await client.post("/api/v1/ai-jobs", json={"job_type": "embed_paper", "payload": {}})
        ).json()

        r = await client.get("/api/v1/ai-jobs")
        assert r.status_code == 200
        assert len(r.json()) == 1

        r = await client.get(f"/api/v1/ai-jobs/{job['id']}")
        assert r.status_code == 200
        assert r.json()["job_type"] == "embed_paper"

    async def test_job_isolated_per_owner(self, client: AsyncClient) -> None:
        await register_user(client, "jobowner@example.com")
        job = (await client.post("/api/v1/ai-jobs", json={"job_type": "x", "payload": {}})).json()

        other = new_client()
        await register_user(other, "otherjob@example.com")
        r = await other.get(f"/api/v1/ai-jobs/{job['id']}")
        assert r.status_code == 404
        await other.aclose()
