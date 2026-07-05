"""Verifies the Alembic migration chain applies and reverses cleanly.

Deliberately synchronous (not `pytest.mark.anyio`): Alembic's `env.py`
manages its own asyncio event loop internally (`asyncio.run(...)`),
which cannot be nested inside a test that's already running inside an
anyio-managed loop. Running these as plain sync tests avoids that.
"""

import asyncio
from pathlib import Path

import psycopg2
import pytest
from alembic import command
from alembic.config import Config
from app.core.config import get_settings
from app.db.session import engine

BACKEND_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _dispose_shared_engine_after_test():
    """Alembic's `env.py` opens its own asyncpg connections inside a
    throwaway `asyncio.run()` loop. The app's shared async `engine`
    (module-level, reused by every other test) must not hold onto any
    pooled connection that was ever touched inside that now-closed
    loop, or later async tests fail with "attached to a different
    loop". Disposing after each test here forces a clean pool."""
    yield
    asyncio.run(engine.dispose(close=False))


def _alembic_config() -> Config:
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "alembic"))
    return config


def _sync_dsn() -> str:
    """Alembic's env.py uses an async driver; table introspection here
    uses a plain sync connection instead, so this test doesn't need its
    own asyncio event-loop management at all."""
    settings = get_settings()
    url = str(settings.DATABASE_URL)
    return url.replace("postgresql+asyncpg://", "postgresql://")


def _table_names() -> set[str]:
    conn = psycopg2.connect(_sync_dsn())
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            )
            return {row[0] for row in cur.fetchall()}
    finally:
        conn.close()


EXPECTED_TABLES = {
    "users",
    "sessions",
    "auth_providers",
    "user_preferences",
    "folders",
    "tags",
    "paper_tags",
    "research_papers",
    "paper_metadata",
    "uploaded_files",
    "chat_sessions",
    "chat_messages",
    "notifications",
    "activity_logs",
    "ai_jobs",
    "team_workspaces",
    "team_members",
}


class TestMigrations:
    def test_upgrade_head_creates_all_expected_tables(self) -> None:
        config = _alembic_config()
        command.upgrade(config, "head")

        assert EXPECTED_TABLES.issubset(_table_names())

    def test_downgrade_and_reupgrade_round_trips(self) -> None:
        config = _alembic_config()
        command.upgrade(config, "head")

        command.downgrade(config, "-1")
        remaining = _table_names()
        assert "research_papers" not in remaining

        command.upgrade(config, "head")
        assert "research_papers" in _table_names()
