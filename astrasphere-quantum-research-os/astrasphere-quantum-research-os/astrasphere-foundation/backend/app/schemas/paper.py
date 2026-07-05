from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema
from app.schemas.tag import TagResponse


class PaperMetadataUpsert(BaseModel):
    doi: str | None = Field(default=None, max_length=255)
    arxiv_id: str | None = Field(default=None, max_length=64)
    abstract: str | None = None
    citation_count: int | None = Field(default=None, ge=0)
    published_date: date | None = None
    extra: dict[str, object] = Field(default_factory=dict)


class PaperMetadataResponse(TimestampedSchema):
    id: UUID
    paper_id: UUID
    doi: str | None
    arxiv_id: str | None
    abstract: str | None
    citation_count: int | None
    published_date: date | None
    extra: dict[str, object]


class ResearchPaperCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    authors: list[str] = Field(default_factory=list)
    venue: str | None = Field(default=None, max_length=255)
    year: int | None = Field(default=None, ge=1900, le=2100)
    folder_id: UUID | None = None
    status: str = Field(default="new", pattern="^(new|reading|reviewed|saved|archived)$")
    tag_ids: list[UUID] = Field(default_factory=list)


class ResearchPaperUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    authors: list[str] | None = None
    venue: str | None = Field(default=None, max_length=255)
    year: int | None = Field(default=None, ge=1900, le=2100)
    folder_id: UUID | None = None
    status: str | None = Field(default=None, pattern="^(new|reading|reviewed|saved|archived)$")
    progress: int | None = Field(default=None, ge=0, le=100)
    tag_ids: list[UUID] | None = None


class ResearchPaperResponse(TimestampedSchema):
    id: UUID
    owner_id: UUID
    folder_id: UUID | None
    title: str
    authors: list[str]
    venue: str | None
    year: int | None
    status: str
    progress: int
    tags: list[TagResponse] = Field(default_factory=list)
    metadata_record: PaperMetadataResponse | None = None
