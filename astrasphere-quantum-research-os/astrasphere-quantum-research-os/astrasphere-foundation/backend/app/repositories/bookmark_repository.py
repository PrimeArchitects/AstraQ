from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bookmark import Bookmark
from app.repositories.base import BaseRepository


class BookmarkRepository(BaseRepository[Bookmark]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Bookmark)

    async def get_for_user_and_paper(self, user_id: UUID, paper_id: UUID) -> Bookmark | None:
        result = await self._session.execute(
            select(Bookmark).where(Bookmark.user_id == user_id, Bookmark.paper_id == paper_id)
        )
        return result.scalar_one_or_none()

    async def list_paginated_for_user(
        self, user_id: UUID, offset: int = 0, limit: int = 20
    ) -> tuple[list[Bookmark], int]:
        query = (
            select(Bookmark)
            .where(Bookmark.user_id == user_id)
            .order_by(Bookmark.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        count_query = select(func.count()).select_from(Bookmark).where(Bookmark.user_id == user_id)
        total = (await self._session.execute(count_query)).scalar_one()
        result = await self._session.execute(query)
        return list(result.scalars().all()), total
