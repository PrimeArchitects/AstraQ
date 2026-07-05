"""User-owned folders for organizing research papers.

Self-referential `parent_id` supports nested folders (a tree, not just
flat categories) without a separate closure table — fine at the depths
a personal research library actually uses.
"""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ModelBase, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.research_paper import ResearchPaper
    from app.models.user import User


class Folder(ModelBase, SoftDeleteMixin):
    __tablename__ = "folders"
    __table_args__ = (
        UniqueConstraint("owner_id", "parent_id", "name", name="uq_folder_owner_parent_name"),
    )

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("folders.id", ondelete="CASCADE"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    color: Mapped[str | None] = mapped_column(String(16), nullable=True)

    owner: Mapped["User"] = relationship()
    children: Mapped[list["Folder"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
    parent: Mapped["Folder | None"] = relationship(
        back_populates="children", remote_side="Folder.id"
    )
    papers: Mapped[list["ResearchPaper"]] = relationship(back_populates="folder")
