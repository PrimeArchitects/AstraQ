"""
Redis-backed fixed-window rate limiter for authentication endpoints.

Kept intentionally simple (fixed window, not sliding/token-bucket) —
auth endpoints need "stop credential stuffing / brute force", not
perfectly smooth traffic shaping. Reuses the app's existing Redis
connection rather than adding a new rate-limiting dependency.
"""

from fastapi import Request
from redis.asyncio import Redis

from app.core.exceptions import RateLimitError


def client_ip(request: Request) -> str:
    """Best-effort client IP, honoring a trusted proxy's X-Forwarded-For."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def enforce_rate_limit(
    redis: Redis, *, key: str, limit: int, window_seconds: int = 60
) -> None:
    """
    Increments a fixed-window counter for `key` and raises
    `RateLimitError` once `limit` is exceeded within `window_seconds`.
    The window resets `window_seconds` after the first request in it,
    not on a wall-clock boundary — simpler and avoids a thundering-herd
    reset at :00.
    """
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, window_seconds)
    if current > limit:
        raise RateLimitError("Too many attempts. Please try again in a moment.")
