from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema


class FolderCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    parent_id: UUID | None = None
    color: str | None = Field(default=None, max_length=16)


class FolderUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    parent_id: UUID | None = None
    color: str | None = Field(default=None, max_length=16)


class FolderResponse(TimestampedSchema):
    id: UUID
    owner_id: UUID
    parent_id: UUID | None
    name: str
    color: str | None
