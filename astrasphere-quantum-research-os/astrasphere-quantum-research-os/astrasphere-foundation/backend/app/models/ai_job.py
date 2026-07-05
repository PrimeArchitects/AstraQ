"""Placeholder job-tracking table for future asynchronous AI work
(paper summarization, embedding generation, etc.).

No job is ever actually enqueued or executed in this step — this is
schema-only groundwork so a future job runner has somewhere durable to
record state without a migration blocking that feature's rollout.
"""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ModelBase

if TYPE_CHECKING:
    from app.models.user import User

AI_JOB_STATUSES = ("queued", "running", "completed", "failed")


class AIJob(ModelBase):
    __tablename__ = "ai_jobs"

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued", index=True)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    result: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    error: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    owner: Mapped["User"] = relationship()
