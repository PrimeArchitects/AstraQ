"""Shared pytest fixtures for the backend test suite.

Uses anyio's pytest plugin (not pytest-asyncio) deliberately: FastAPI,
Starlette, and httpx are all built on anyio, and running tests through
pytest-asyncio's independently-managed event loop caused persistent
loop-mismatch errors against redis-py's raw-asyncio connections. anyio's
plugin shares the loop model these libraries already expect.

DB/Redis cleanup is attached to the `client` fixture rather than made
globally autouse: purely-sync unit tests (test_security.py,
test_validation.py) never request `client`, so they never trigger
async fixture teardown that anyio's plugin has no loop to run for a
non-async test.

Runs against a real Postgres/Redis (the same ones used for local dev —
see docker-compose.yml / CI's service containers), truncating auth
tables between tests rather than using a mocked DB. This is deliberate:
password hashing, unique constraints, cascades, and transaction
boundaries are exactly the things worth catching with a real database.
"""

from collections.abc import AsyncGenerator

import pytest
from app.db.redis_client import force_reset_redis_client_for_tests, get_redis
from app.db.session import AsyncSessionLocal, engine
from app.main import app
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    # Each test gets its own event loop (anyio's default). Connections
    # pooled by a previous test are bound to that test's now-closed
    # loop, so drop them here — without attempting a graceful close,
    # which would itself fail against a dead loop — before anything
    # in this test creates fresh ones.
    await engine.dispose(close=False)
    force_reset_redis_client_for_tests()

    async with AsyncSessionLocal() as session:
        await session.execute(
            text("TRUNCATE users, sessions, user_preferences, auth_providers CASCADE")
        )
        await session.commit()
    redis = await get_redis()
    await redis.flushdb()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
