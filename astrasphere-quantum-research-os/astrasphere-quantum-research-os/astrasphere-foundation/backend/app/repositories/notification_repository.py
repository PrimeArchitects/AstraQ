from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Notification)

    async def get_for_user(self, notification_id: UUID, user_id: UUID) -> Notification | None:
        result = await self._session.execute(
            select(Notification).where(
                Notification.id == notification_id, Notification.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def list_for_user(
        self, user_id: UUID, offset: int = 0, limit: int = 20
    ) -> list[Notification]:
        result = await self._session.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_for_user(self, user_id: UUID) -> int:
        from sqlalchemy import func

        result = await self._session.execute(
            select(func.count()).select_from(Notification).where(Notification.user_id == user_id)
        )
        return result.scalar_one()

    async def mark_all_read(self, user_id: UUID) -> int:
        result = await self._session.execute(
            update(Notification)
            .where(Notification.user_id == user_id, Notification.read_at.is_(None))
            .values(read_at=datetime.now(UTC))
        )
        await self._session.flush()
        rowcount: int = result.rowcount if result.rowcount is not None else 0  # type: ignore[attr-defined]
        return rowcount

    async def unread_count(self, user_id: UUID) -> int:
        from sqlalchemy import func

        result = await self._session.execute(
            select(func.count())
            .select_from(Notification)
            .where(Notification.user_id == user_id, Notification.read_at.is_(None))
        )
        return result.scalar_one()
