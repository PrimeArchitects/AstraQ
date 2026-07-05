from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.folder import Folder
from app.repositories.base import BaseRepository


class FolderRepository(BaseRepository[Folder]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Folder)

    async def list_for_owner(self, owner_id: UUID) -> list[Folder]:
        result = await self._session.execute(
            self._base_query().where(Folder.owner_id == owner_id).order_by(Folder.name.asc())
        )
        return list(result.scalars().all())

    async def get_by_name(self, owner_id: UUID, parent_id: UUID | None, name: str) -> Folder | None:
        result = await self._session.execute(
            select(Folder).where(
                Folder.owner_id == owner_id,
                Folder.parent_id == parent_id,
                Folder.name == name,
                Folder.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()
