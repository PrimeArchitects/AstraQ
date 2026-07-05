"""Reusable Pydantic schemas shared across feature domains."""

from datetime import datetime
from typing import Generic, Literal, TypeVar

from fastapi import Query
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
    total_pages: int


class HealthStatus(BaseModel):
    status: str
    app_name: str
    app_env: str
    version: str


SortOrder = Literal["asc", "desc"]


class PageParams:
    """Shared pagination query params, injected via `Depends(PageParams)`.

    1-indexed `page` (not raw offset) because that's what a frontend
    table/paginator UI naturally works with; repositories translate to
    `offset = (page - 1) * page_size` at the query layer.
    """

    def __init__(
        self,
        page: int = Query(1, ge=1, description="1-indexed page number"),
        page_size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    ) -> None:
        self.page = page
        self.page_size = page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    def to_page(self, items: list[T], total: int) -> "Page[T]":
        total_pages = (total + self.page_size - 1) // self.page_size if total else 0
        return Page(
            items=items,
            total=total,
            page=self.page,
            page_size=self.page_size,
            total_pages=total_pages,
        )
