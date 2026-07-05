from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag
from app.repositories.base import BaseRepository


class TagRepository(BaseRepository[Tag]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Tag)

    async def list_for_owner(self, owner_id: UUID) -> list[Tag]:
        result = await self._session.execute(
            select(Tag).where(Tag.owner_id == owner_id).order_by(Tag.name.asc())
        )
        return list(result.scalars().all())

    async def get_by_name(self, owner_id: UUID, name: str) -> Tag | None:
        result = await self._session.execute(
            select(Tag).where(Tag.owner_id == owner_id, Tag.name == name)
        )
        return result.scalar_one_or_none()

    async def get_many_by_ids(self, owner_id: UUID, tag_ids: list[UUID]) -> list[Tag]:
        if not tag_ids:
            return []
        result = await self._session.execute(
            select(Tag).where(Tag.owner_id == owner_id, Tag.id.in_(tag_ids))
        )
        return list(result.scalars().all())
