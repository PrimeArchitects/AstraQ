"""Reusable Pydantic schemas shared across feature domains."""

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ORMModel(BaseModel):
    """Base schema for models that map 1:1 onto ORM entities."""

    model_config = ConfigDict(from_attributes=True)


class TimestampedSchema(ORMModel):
    created_at: datetime
    updated_at: datetime


class Page(BaseModel, Generic[T]):
    """Generic paginated response envelope."""

    items: list[T]
    total: int
    page: int
    page_size: int


class HealthStatus(BaseModel):
    status: str
    app_name: str
    app_env: str
    version: str
