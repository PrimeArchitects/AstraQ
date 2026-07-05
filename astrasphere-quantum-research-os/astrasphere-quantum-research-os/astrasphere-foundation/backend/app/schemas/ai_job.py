from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema


class AIJobCreate(BaseModel):
    """Placeholder job submission — no job is actually executed in
    this step. Registers intent/payload for a future job runner."""

    job_type: str = Field(min_length=1, max_length=64)
    payload: dict[str, object] = Field(default_factory=dict)


class AIJobResponse(TimestampedSchema):
    id: UUID
    owner_id: UUID
    job_type: str
    status: str
    payload: dict[str, object]
    result: dict[str, object] | None
    error: str | None
