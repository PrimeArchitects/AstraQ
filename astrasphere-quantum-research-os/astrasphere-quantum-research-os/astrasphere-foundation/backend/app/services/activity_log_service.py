"""Activity log read access. Entries are written via `app.core.audit`,
inline with the mutation they describe — this service is query-only."""

from app.models.activity_log import ActivityLog
from app.models.user import User
from app.repositories.activity_log_repository import ActivityLogRepository
from app.services.base import BaseService


class ActivityLogService(BaseService):
    def __init__(self, activity_log_repo: ActivityLogRepository) -> None:
        self.activity_logs = activity_log_repo

    async def list_for_user(
        self, user: User, offset: int = 0, limit: int = 20
    ) -> tuple[list[ActivityLog], int]:
        return await self.activity_logs.list_for_user(user.id, offset, limit)
