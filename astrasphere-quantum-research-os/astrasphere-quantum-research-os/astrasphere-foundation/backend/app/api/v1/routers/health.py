"""Health, readiness, liveness, and version endpoints.

- `/health`   — overall status; kept for backward compatibility with
                any existing monitoring already pointed at it.
- `/health/live`  — process is up and can handle requests at all. No
                    dependency checks: if this fails, restart the pod.
- `/health/ready` — process is up AND its dependencies (DB, Redis) are
                    reachable. If this fails, stop routing traffic to
                    it but don't necessarily restart.
- `/version`  — build/version metadata for debugging deployed revisions.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from app.api.deps import Cache, DbSession
from app.core.config import get_settings
from app.schemas.common import HealthStatus

router = APIRouter(tags=["health"])

APP_VERSION = "0.1.0"


class DependencyStatus(BaseModel):
    database: str
    redis: str


class ReadinessStatus(BaseModel):
    status: str
    dependencies: DependencyStatus


class LivenessStatus(BaseModel):
    status: str


class VersionInfo(BaseModel):
    version: str
    app_name: str
    app_env: str


@router.get("/health", response_model=HealthStatus, summary="Overall health status")
async def health_check() -> HealthStatus:
    settings = get_settings()
    return HealthStatus(
        status="ok", app_name=settings.APP_NAME, app_env=settings.APP_ENV, version=APP_VERSION
    )


@router.get("/health/live", response_model=LivenessStatus, summary="Liveness probe")
async def liveness() -> LivenessStatus:
    """No dependency checks by design — this answers only "is the
    process alive", which is what an orchestrator's restart decision
    should be based on."""
    return LivenessStatus(status="alive")


@router.get("/health/ready", response_model=ReadinessStatus, summary="Readiness probe")
async def readiness(db: DbSession, cache: Cache) -> ReadinessStatus:
    """Checks that the dependencies this app actually needs to serve
    traffic are reachable. A failure here should pull the instance out
    of the load balancer, not restart it."""
    db_status = "ok"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:  # noqa: BLE001 - readiness must report, not raise
        db_status = "unavailable"

    redis_status = "ok"
    try:
        await cache.ping()
    except Exception:  # noqa: BLE001 - readiness must report, not raise
        redis_status = "unavailable"

    overall = "ready" if db_status == "ok" and redis_status == "ok" else "not_ready"
    return ReadinessStatus(
        status=overall, dependencies=DependencyStatus(database=db_status, redis=redis_status)
    )


@router.get("/version", response_model=VersionInfo, summary="Build/version information")
async def version_info() -> VersionInfo:
    settings = get_settings()
    return VersionInfo(version=APP_VERSION, app_name=settings.APP_NAME, app_env=settings.APP_ENV)
