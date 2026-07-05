from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import TimestampedSchema


class NotificationResponse(TimestampedSchema):
    id: UUID
    user_id: UUID
    type: str
    title: str
    body: str | None
    link: str | None
    read_at: datetime | None


class NotificationMarkReadResponse(BaseModel):
    updated: int
