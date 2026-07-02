"""Redis connection management (caching, rate limiting, ephemeral state)."""

from functools import lru_cache

from redis.asyncio import ConnectionPool, Redis

from app.core.config import settings


@lru_cache
def get_redis_pool() -> ConnectionPool:
    """Return a cached Redis connection pool for the process lifetime."""
    return ConnectionPool.from_url(settings.redis_url, decode_responses=True)


async def get_redis() -> Redis:
    """FastAPI dependency that returns a Redis client bound to the shared pool."""
    return Redis(connection_pool=get_redis_pool())


async def ping_redis() -> bool:
    """Health-check helper: returns True if Redis responds to PING."""
    client = await get_redis()
    try:
        return bool(await client.ping())
    except Exception:
        return False
