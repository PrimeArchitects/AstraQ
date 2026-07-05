from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema


class UploadedFileCreate(BaseModel):
    """Metadata-only record creation. No file bytes are handled — the
    actual upload endpoint (and the storage write it implies) is out of
    scope for this step; this just registers what a future upload will
    reference."""

    paper_id: UUID | None = None
    filename: str = Field(min_length=1, max_length=500)
    file_size: int = Field(ge=0)
    storage_path: str = Field(min_length=1, max_length=1024)
    checksum: str = Field(min_length=1, max_length=128)
    content_type: str | None = Field(default=None, max_length=120)


class UploadedFileUpdate(BaseModel):
    processing_status: str | None = Field(
        default=None, pattern="^(pending|processing|completed|failed)$"
    )
    paper_id: UUID | None = None


class UploadedFileResponse(TimestampedSchema):
    id: UUID
    owner_id: UUID
    paper_id: UUID | None
    filename: str
    file_size: int
    storage_path: str
    checksum: str
    content_type: str | None
    processing_status: str
