"""Shared FastAPI dependencies re-exported for convenience."""

from app.db.session import get_db
from app.services.qdrant_client import get_qdrant_client
from app.services.redis_client import get_redis

__all__ = ["get_db", "get_redis", "get_qdrant_client"]
