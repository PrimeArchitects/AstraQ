"""Integration tests for chat session/message persistence (no AI calls)."""

import pytest
from httpx import AsyncClient

from tests.conftest import register_user

pytestmark = pytest.mark.anyio


class TestChat:
    async def test_create_session_and_list(self, client: AsyncClient) -> None:
        await register_user(client)
        r = await client.post("/api/v1/chat/sessions", json={"title": "My research chat"})
        assert r.status_code == 201, r.text

        r = await client.get("/api/v1/chat/sessions")
        assert r.status_code == 200
        assert len(r.json()) == 1

    async def test_session_scoped_to_paper(self, client: AsyncClient) -> None:
        await register_user(client)
        paper = (await client.post("/api/v1/papers", json={"title": "Chat paper"})).json()
        r = await client.post(
            "/api/v1/chat/sessions", json={"title": "About this paper", "paper_id": paper["id"]}
        )
        assert r.status_code == 201
        assert r.json()["paper_id"] == paper["id"]

    async def test_add_messages_and_get_detail(self, client: AsyncClient) -> None:
        await register_user(client)
        session = (await client.post("/api/v1/chat/sessions", json={})).json()

        r = await client.post(
            f"/api/v1/chat/sessions/{session['id']}/messages",
            json={"role": "user", "content": "Summarize this paper."},
        )
        assert r.status_code == 201, r.text

        r = await client.get(f"/api/v1/chat/sessions/{session['id']}")
        assert r.status_code == 200
        assert len(r.json()["messages"]) == 1
        assert r.json()["messages"][0]["content"] == "Summarize this paper."

    async def test_invalid_message_role_rejected(self, client: AsyncClient) -> None:
        await register_user(client)
        session = (await client.post("/api/v1/chat/sessions", json={})).json()
        r = await client.post(
            f"/api/v1/chat/sessions/{session['id']}/messages",
            json={"role": "bogus", "content": "x"},
        )
        assert r.status_code == 422

    async def test_delete_session(self, client: AsyncClient) -> None:
        await register_user(client)
        session = (await client.post("/api/v1/chat/sessions", json={})).json()
        r = await client.delete(f"/api/v1/chat/sessions/{session['id']}")
        assert r.status_code == 204

        r = await client.get(f"/api/v1/chat/sessions/{session['id']}")
        assert r.status_code == 404
