from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.uploaded_file import UploadedFile
from app.repositories.base import BaseRepository


class FileRepository(BaseRepository[UploadedFile]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UploadedFile)

    async def get_for_owner(self, file_id: UUID, owner_id: UUID) -> UploadedFile | None:
        result = await self._session.execute(
            self._base_query().where(UploadedFile.id == file_id, UploadedFile.owner_id == owner_id)
        )
        return result.scalar_one_or_none()

    async def list_paginated_for_owner(
        self, owner_id: UUID, offset: int = 0, limit: int = 20
    ) -> tuple[list[UploadedFile], int]:
        query = (
            self._base_query()
            .where(UploadedFile.owner_id == owner_id)
            .order_by(UploadedFile.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        count_query = (
            select(func.count())
            .select_from(UploadedFile)
            .where(UploadedFile.owner_id == owner_id, UploadedFile.deleted_at.is_(None))
        )
        total = (await self._session.execute(count_query)).scalar_one()
        result = await self._session.execute(query)
        return list(result.scalars().all()), total
