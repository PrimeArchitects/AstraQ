from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema


class ChatSessionCreate(BaseModel):
    title: str = Field(default="New conversation", max_length=255)
    paper_id: UUID | None = None


class ChatSessionUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)


class ChatMessageCreate(BaseModel):
    role: str = Field(pattern="^(user|assistant|system)$")
    content: str = Field(min_length=1)


class ChatMessageResponse(TimestampedSchema):
    id: UUID
    session_id: UUID
    role: str
    content: str


class ChatSessionResponse(TimestampedSchema):
    id: UUID
    owner_id: UUID
    paper_id: UUID | None
    title: str


class ChatSessionDetailResponse(ChatSessionResponse):
    messages: list[ChatMessageResponse] = Field(default_factory=list)
