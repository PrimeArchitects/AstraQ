"""Core research paper record.

Deliberately holds only user-entered/curated fields (title, authors,
status, ownership, folder placement). Extraction-derived metadata
(DOI, citation counts, abstract text pulled from a PDF) lives in
`PaperMetadata` instead, so a future PDF-parsing pipeline only ever
writes to one narrow table rather than touching this one.
"""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ARRAY, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ModelBase, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.bookmark import Bookmark
    from app.models.chat_session import ChatSession
    from app.models.folder import Folder
    from app.models.paper_metadata import PaperMetadata
    from app.models.tag import Tag
    from app.models.uploaded_file import UploadedFile
    from app.models.user import User

PAPER_STATUSES = ("new", "reading", "reviewed", "saved", "archived")


class ResearchPaper(ModelBase, SoftDeleteMixin):
    __tablename__ = "research_papers"

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    folder_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("folders.id", ondelete="SET NULL"), nullable=True, index=True
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    authors: Mapped[list[str]] = mapped_column(ARRAY(String(200)), nullable=False, default=list)
    venue: Mapped[str | None] = mapped_column(String(255), nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="new", index=True)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    owner: Mapped["User"] = relationship()
    folder: Mapped["Folder | None"] = relationship(back_populates="papers")
    metadata_record: Mapped["PaperMetadata | None"] = relationship(
        back_populates="paper", cascade="all, delete-orphan", uselist=False
    )
    files: Mapped[list["UploadedFile"]] = relationship(
        back_populates="paper", cascade="all, delete-orphan"
    )
    bookmarks: Mapped[list["Bookmark"]] = relationship(
        back_populates="paper", cascade="all, delete-orphan"
    )
    chat_sessions: Mapped[list["ChatSession"]] = relationship(back_populates="paper")
    tags: Mapped[list["Tag"]] = relationship(secondary="paper_tags", back_populates="papers")
