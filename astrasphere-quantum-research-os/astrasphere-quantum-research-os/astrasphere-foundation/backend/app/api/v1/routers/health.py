"""Liveness/readiness endpoint. No auth, no DB dependency required to pass."""

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.common import HealthStatus

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthStatus, summary="Liveness/readiness probe")
async def health_check() -> HealthStatus:
    settings = get_settings()
    return HealthStatus(
        status="ok",
        app_name=settings.APP_NAME,
        app_env=settings.APP_ENV,
        version="0.1.0",
    )
