"""User-scoped tags and the paper<->tag association table.

Tags are per-user (not global) — a shared global tag namespace would
need moderation/collision handling this project has no use for yet.
"""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, ModelBase

if TYPE_CHECKING:
    from app.models.research_paper import ResearchPaper
    from app.models.user import User

paper_tags = Table(
    "paper_tags",
    Base.metadata,
    Column(
        "paper_id",
        PGUUID(as_uuid=True),
        ForeignKey("research_papers.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id", PGUUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Tag(ModelBase):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("owner_id", "name", name="uq_tag_owner_name"),)

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    color: Mapped[str | None] = mapped_column(String(16), nullable=True)

    owner: Mapped["User"] = relationship()
    papers: Mapped[list["ResearchPaper"]] = relationship(
        secondary=paper_tags, back_populates="tags"
    )
