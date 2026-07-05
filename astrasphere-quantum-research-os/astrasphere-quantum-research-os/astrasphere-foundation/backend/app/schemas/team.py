from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema


class TeamWorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class TeamWorkspaceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None


class TeamWorkspaceResponse(TimestampedSchema):
    id: UUID
    owner_id: UUID
    name: str
    description: str | None


class TeamMemberCreate(BaseModel):
    user_id: UUID
    role: str = Field(default="member", pattern="^(owner|admin|member)$")


class TeamMemberResponse(TimestampedSchema):
    id: UUID
    workspace_id: UUID
    user_id: UUID
    role: str
