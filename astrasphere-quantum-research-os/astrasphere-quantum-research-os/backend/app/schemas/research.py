"""Pydantic schemas for the research API."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ResearchStatus(str, Enum):
    draft = "draft"
    active = "active"
    completed = "completed"
    archived = "archived"


class ResearchProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    summary: str = Field(default="", max_length=5000)
    status: ResearchStatus = Field(default=ResearchStatus.draft)


class ResearchProjectCreate(ResearchProjectBase):
    pass


class ResearchProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    summary: str | None = Field(default=None, max_length=5000)
    status: ResearchStatus | None = None


class ResearchProjectRead(ResearchProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class VectorSearchQuery(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)


class VectorSearchResult(BaseModel):
    id: str
    score: float
    payload: dict
