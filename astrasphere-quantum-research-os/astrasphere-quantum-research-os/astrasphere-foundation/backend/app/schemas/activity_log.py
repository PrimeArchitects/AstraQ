from uuid import UUID

from app.schemas.common import TimestampedSchema


class ActivityLogResponse(TimestampedSchema):
    id: UUID
    user_id: UUID | None
    action: str
    resource_type: str
    resource_id: str | None
    extra_data: dict[str, object]
    ip_address: str | None
