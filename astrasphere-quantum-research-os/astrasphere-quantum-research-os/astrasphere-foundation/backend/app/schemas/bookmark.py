from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema


class BookmarkCreate(BaseModel):
    paper_id: UUID
    note: str | None = Field(default=None, max_length=1000)


class BookmarkUpdate(BaseModel):
    note: str | None = Field(default=None, max_length=1000)


class BookmarkResponse(TimestampedSchema):
    id: UUID
    user_id: UUID
    paper_id: UUID
    note: str | None
