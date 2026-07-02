"""Aggregates all v1 API endpoint routers."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, research, vectors

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(research.router, prefix="/research", tags=["research"])
api_router.include_router(vectors.router, prefix="/vectors", tags=["vectors"])
