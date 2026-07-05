"""Smoke test for the health endpoint — verifies the app boots and routes."""

import pytest


@pytest.mark.anyio
async def test_health_check(client) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["app_name"] == "AstraSphere Quantum Research OS"


@pytest.mark.anyio
async def test_liveness_has_no_dependencies(client) -> None:
    response = await client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


@pytest.mark.anyio
async def test_readiness_reports_dependency_status(client) -> None:
    response = await client.get("/api/v1/health/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["dependencies"]["database"] == "ok"
    assert body["dependencies"]["redis"] == "ok"


@pytest.mark.anyio
async def test_version_endpoint(client) -> None:
    response = await client.get("/api/v1/version")
    assert response.status_code == 200
    body = response.json()
    assert "version" in body
    assert body["app_name"] == "AstraSphere Quantum Research OS"
