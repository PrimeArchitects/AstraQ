"""Aggregates all v1 routers under a single APIRouter.

New feature routers register here. Versioning lives at the URL level
(`/api/v1`, later `/api/v2`) so breaking changes can be introduced
without disrupting existing API consumers.
"""

from fastapi import APIRouter

from app.api.v1.routers import (
    activity_logs,
    ai_jobs,
    auth,
    bookmarks,
    chat,
    files,
    folders,
    health,
    notifications,
    papers,
    tags,
    teams,
    users,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(folders.router)
api_router.include_router(tags.router)
api_router.include_router(papers.router)
api_router.include_router(bookmarks.router)
api_router.include_router(files.router)
api_router.include_router(chat.router)
api_router.include_router(notifications.router)
api_router.include_router(activity_logs.router)
api_router.include_router(ai_jobs.router)
api_router.include_router(teams.router)
