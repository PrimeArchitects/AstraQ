"""Notification business logic (in-app only, no delivery channels)."""

import uuid
from datetime import UTC, datetime

from app.core.exceptions import NotFoundError
from app.models.notification import Notification
from app.models.user import User
from app.repositories.notification_repository import NotificationRepository
from app.services.base import BaseService


class NotificationService(BaseService):
    def __init__(self, notification_repo: NotificationRepository) -> None:
        self.notifications = notification_repo

    async def list_for_user(
        self, user: User, offset: int = 0, limit: int = 20
    ) -> list[Notification]:
        return await self.notifications.list_for_user(user.id, offset, limit)

    async def unread_count(self, user: User) -> int:
        return await self.notifications.unread_count(user.id)

    async def total_count(self, user: User) -> int:
        return await self.notifications.count_for_user(user.id)

    async def mark_read(self, user: User, notification_id: uuid.UUID) -> Notification:
        notification = await self.notifications.get_for_user(notification_id, user.id)
        if notification is None:
            raise NotFoundError("Notification not found.")
        notification.read_at = datetime.now(UTC)
        await self.notifications.session.flush()
        await self.notifications.session.refresh(notification)
        return notification

    async def mark_all_read(self, user: User) -> int:
        return await self.notifications.mark_all_read(user.id)
