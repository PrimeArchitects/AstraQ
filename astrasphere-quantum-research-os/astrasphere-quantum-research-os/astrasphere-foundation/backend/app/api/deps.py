"""Shared FastAPI dependencies (DB sessions, cache, vector store, current user).

`get_current_user` is a placeholder: it always raises until the auth
system is implemented in a later phase. Routers that will require auth
should depend on it now so the wiring doesn't need to change later.
"""

from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.db.qdrant_client import get_qdrant
from app.db.redis_client import get_redis
from app.db.session import get_db_session

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
Cache = Annotated[Redis, Depends(get_redis)]
VectorStore = Annotated[object, Depends(get_qdrant)]


async def get_current_user() -> dict[str, object]:
    """Placeholder auth dependency — not wired to any router yet.

    Real implementation (JWT/session validation, user lookup) lands in
    the authentication phase. Kept here so future routers can start
    depending on `CurrentUser` without another refactor.
    """
    raise UnauthorizedError("Authentication is not yet implemented.")
