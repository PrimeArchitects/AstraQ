"""Liveness and readiness endpoints."""

from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import AsyncSessionLocal
from app.services.qdrant_client import ping_qdrant
from app.services.redis_client import ping_redis

router = APIRouter()


@router.get("", summary="Basic liveness check")
async def health() -> dict[str, str]:
    """Simple liveness probe used by Docker healthchecks and load balancers."""
    return {"status": "ok"}


@router.get("/ready", summary="Readiness check across all dependencies")
async def readiness() -> dict[str, object]:
    """Verify connectivity to Postgres, Redis, and Qdrant."""
    checks: dict[str, bool] = {}

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        checks["postgres"] = True
    except Exception:
        checks["postgres"] = False

    checks["redis"] = await ping_redis()
    checks["qdrant"] = await ping_qdrant()

    overall = all(checks.values())
    return {"status": "ok" if overall else "degraded", "checks": checks}
