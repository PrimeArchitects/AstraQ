"""Audit logging helper.

Services call `record_activity` alongside a mutation, using the same
`AsyncSession` (and therefore the same transaction) as the mutation
itself, so the audit row and the change it describes always commit or
roll back together.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity_log import ActivityLog


async def record_activity(
    session: AsyncSession,
    *,
    user_id: uuid.UUID | None,
    action: str,
    resource_type: str,
    resource_id: str | None = None,
    extra_data: dict[str, object] | None = None,
    ip_address: str | None = None,
) -> ActivityLog:
    entry = ActivityLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        extra_data=extra_data or {},
        ip_address=ip_address,
    )
    session.add(entry)
    await session.flush()
    return entry
