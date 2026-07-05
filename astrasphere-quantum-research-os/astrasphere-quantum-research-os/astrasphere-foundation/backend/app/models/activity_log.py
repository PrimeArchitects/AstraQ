"""Append-only audit trail.

Written by the service layer (see `app/core/audit.py`) alongside the
mutation it's recording, in the same transaction — so an activity log
row and the change it describes commit or roll back together. Never
updated or soft-deleted after creation.
"""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ModelBase

if TYPE_CHECKING:
    from app.models.user import User


class ActivityLog(ModelBase):
    __tablename__ = "activity_logs"

    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    resource_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    extra_data: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)

    user: Mapped["User | None"] = relationship()
