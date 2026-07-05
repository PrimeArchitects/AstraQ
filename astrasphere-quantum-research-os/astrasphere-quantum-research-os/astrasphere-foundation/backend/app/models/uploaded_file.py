"""File metadata records.

Metadata-only by design (see Prompt 4 scope): this table describes a
file that a future upload endpoint will place into storage — it holds
no bytes and this step wires up no upload endpoint. `storage_path` is
a logical key (e.g. an eventual S3/GCS object key), not a local path.
"""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ModelBase, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.research_paper import ResearchPaper
    from app.models.user import User

PROCESSING_STATUSES = ("pending", "processing", "completed", "failed")


class UploadedFile(ModelBase, SoftDeleteMixin):
    __tablename__ = "uploaded_files"

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    paper_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("research_papers.id", ondelete="CASCADE"), nullable=True, index=True
    )

    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    checksum: Mapped[str] = mapped_column(String(128), nullable=False)
    content_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    processing_status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="pending", index=True
    )

    owner: Mapped["User"] = relationship()
    paper: Mapped["ResearchPaper | None"] = relationship(back_populates="files")
