"""Smoke test for the health endpoint — verifies the app boots and routes."""

import pytest


@pytest.mark.anyio
async def test_health_check(client) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["app_name"] == "AstraSphere Quantum Research OS"
