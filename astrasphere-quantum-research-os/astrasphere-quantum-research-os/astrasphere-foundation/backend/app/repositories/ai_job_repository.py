from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_job import AIJob
from app.repositories.base import BaseRepository


class AIJobRepository(BaseRepository[AIJob]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AIJob)

    async def get_for_owner(self, job_id: UUID, owner_id: UUID) -> AIJob | None:
        result = await self._session.execute(
            select(AIJob).where(AIJob.id == job_id, AIJob.owner_id == owner_id)
        )
        return result.scalar_one_or_none()

    async def list_for_owner(self, owner_id: UUID, offset: int = 0, limit: int = 20) -> list[AIJob]:
        result = await self._session.execute(
            select(AIJob)
            .where(AIJob.owner_id == owner_id)
            .order_by(AIJob.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())
