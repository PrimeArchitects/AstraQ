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
        await _redis_client.aclose()
        _redis_client = None


def force_reset_redis_client_for_tests() -> None:
    """Test-only: drops the cached client *without* attempting a graceful
    close. anyio/pytest gives each test its own event loop, and a
    connection's close() tries to communicate on that original loop —
    which is already closed by the time the next test runs. Discarding
    the reference (letting the OS clean up the dead socket) avoids that
    crash; the next `get_redis()` call creates a fresh client bound to
    the current loop."""
    global _redis_client
    _redis_client = None
