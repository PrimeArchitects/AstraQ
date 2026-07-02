"""Aggregates all v1 routers under a single APIRouter.

New feature routers register here. Versioning lives at the URL level
(`/api/v1`, later `/api/v2`) so breaking changes can be introduced
without disrupting existing API consumers.
"""

from fastapi import APIRouter

from app.api.v1.routers import health

api_router = APIRouter()
api_router.include_router(health.router)
