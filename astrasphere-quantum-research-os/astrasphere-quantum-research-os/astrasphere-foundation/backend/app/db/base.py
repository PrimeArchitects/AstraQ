"""Declarative base for all ORM models, plus shared mixins."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """All models inherit from this. Import target for Alembic autogenerate."""


class UUIDPrimaryKeyMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class SoftDeleteMixin:
    """`deleted_at` nullable timestamp. Non-null means the row is
    logically deleted; repositories filter these out by default rather
    than issuing a real DELETE, so relationships and audit history
    survive a user "removing" something."""

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class ModelBase(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Every concrete feature model has at least a UUID `id` and
    timestamps; `BaseRepository` is generic over this (rather than raw
    `Base`) so mypy knows those attributes exist without per-repository
    `# type: ignore`s. `SoftDeleteMixin` stays separate since it's
    optional per model and checked with `isinstance`/`issubclass` at
    runtime."""

    __abstract__ = True
