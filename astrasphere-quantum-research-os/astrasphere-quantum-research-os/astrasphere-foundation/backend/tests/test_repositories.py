"""Repository-level tests: pagination, filtering, sorting, and soft
delete against a real Postgres session (no HTTP layer)."""

import pytest
from app.db.session import AsyncSessionLocal, engine
from app.models.folder import Folder
from app.models.tag import Tag
from app.models.user import User
from app.repositories.folder_repository import FolderRepository
from app.repositories.tag_repository import TagRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

pytestmark = pytest.mark.anyio


@pytest.fixture(autouse=True)
async def _drop_stale_pooled_connections() -> None:
    """Each test gets its own event loop (anyio's default); a
    connection pooled by a previous test is bound to that now-closed
    loop. Drop it here without attempting a graceful close (which
    would itself fail against a dead loop) — mirrors the `client`
    fixture in conftest.py for tests that talk to the DB directly."""
    await engine.dispose(close=False)


async def _create_user(session, email: str) -> User:
    from app.core.email import ConsoleEmailSender
    from app.repositories.session_repository import SessionRepository

    auth_service = AuthService(
        UserRepository(session), SessionRepository(session), ConsoleEmailSender()
    )
    user = await auth_service.register(
        email=email, password="SecurePass123", display_name="Repo Test"
    )
    await session.commit()
    return user


class TestBaseRepositorySoftDelete:
    async def test_soft_deleted_row_excluded_from_get_and_list(self) -> None:
        async with AsyncSessionLocal() as session:
            user = await _create_user(session, "repo1@example.com")
            folder_repo = FolderRepository(session)
            folder = await folder_repo.create(Folder(owner_id=user.id, name="Temp"))
            await session.commit()

            await folder_repo.soft_delete(folder)
            await session.commit()

            assert await folder_repo.get(folder.id) is None
            visible = await folder_repo.list_for_owner(user.id)
            assert folder.id not in [f.id for f in visible]

    async def test_get_with_include_deleted_still_finds_row(self) -> None:
        async with AsyncSessionLocal() as session:
            user = await _create_user(session, "repo2@example.com")
            folder_repo = FolderRepository(session)
            folder = await folder_repo.create(Folder(owner_id=user.id, name="Temp2"))
            await session.commit()

            await folder_repo.soft_delete(folder)
            await session.commit()

            found = await folder_repo.get(folder.id, include_deleted=True)
            assert found is not None
            assert found.is_deleted is True


class TestTagRepository:
    async def test_get_many_by_ids_only_returns_owned_tags(self) -> None:
        async with AsyncSessionLocal() as session:
            owner = await _create_user(session, "repo3@example.com")
            other = await _create_user(session, "repo4@example.com")
            tag_repo = TagRepository(session)

            owned_tag = await tag_repo.create(Tag(owner_id=owner.id, name="mine"))
            other_tag = await tag_repo.create(Tag(owner_id=other.id, name="theirs"))
            await session.commit()

            result = await tag_repo.get_many_by_ids(owner.id, [owned_tag.id, other_tag.id])
            assert [t.id for t in result] == [owned_tag.id]
