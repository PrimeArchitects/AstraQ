"""Redis connection factory (caching, rate limiting, task queues, session cache)."""

from redis.asyncio import Redis, from_url

from app.core.config import get_settings

_redis_client: Redis | None = None


async def get_redis() -> Redis:
    """FastAPI dependency: returns a shared Redis connection pool."""
    global _redis_client
    if _redis_client is None:
        settings = get_settings()
        _redis_client = from_url(str(settings.REDIS_URL), decode_responses=True)  # type: ignore[no-untyped-call]
    return _redis_client


async def close_redis() -> None:
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None
