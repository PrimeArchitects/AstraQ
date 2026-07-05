from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity_log import ActivityLog
from app.repositories.base import BaseRepository


class ActivityLogRepository(BaseRepository[ActivityLog]):
    """Read access to the audit trail. Writes go through
    `app.core.audit.record_activity`, not through this repository, so
    that log entries are always created inside the same transaction as
    the action they describe."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ActivityLog)

    async def list_for_user(
        self, user_id: UUID, offset: int = 0, limit: int = 20
    ) -> tuple[list[ActivityLog], int]:
        from sqlalchemy import func, select

        query = (
            select(ActivityLog)
            .where(ActivityLog.user_id == user_id)
            .order_by(ActivityLog.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        count_query = (
            select(func.count()).select_from(ActivityLog).where(ActivityLog.user_id == user_id)
        )
        total = (await self._session.execute(count_query)).scalar_one()
        result = await self._session.execute(query)
        return list(result.scalars().all()), total
