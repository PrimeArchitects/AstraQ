from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema


class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    color: str | None = Field(default=None, max_length=16)


class TagUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    color: str | None = Field(default=None, max_length=16)


class TagResponse(TimestampedSchema):
    id: UUID
    owner_id: UUID
    name: str
    color: str | None
