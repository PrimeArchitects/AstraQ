"""A user's bookmark on a paper. Separate from `ResearchPaper.status`
("saved") because a bookmark carries its own note and can be toggled
independently of the paper's reading-status workflow."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ModelBase

if TYPE_CHECKING:
    from app.models.research_paper import ResearchPaper
    from app.models.user import User


class Bookmark(ModelBase):
    __tablename__ = "bookmarks"
    __table_args__ = (UniqueConstraint("user_id", "paper_id", name="uq_bookmark_user_paper"),)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    paper_id: Mapped[UUID] = mapped_column(
        ForeignKey("research_papers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    note: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    user: Mapped["User"] = relationship()
    paper: Mapped["ResearchPaper"] = relationship(back_populates="bookmarks")
