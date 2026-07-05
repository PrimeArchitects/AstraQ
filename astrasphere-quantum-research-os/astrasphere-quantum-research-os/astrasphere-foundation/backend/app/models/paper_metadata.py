"""Extraction/enrichment metadata for a research paper.

Split 1:1 from `ResearchPaper` because this table is the write target
for a future PDF-parsing/enrichment job — isolating it means that
pipeline never needs write access to the user-curated paper fields.
`extra` is an open JSON bucket for whatever a later extractor produces
before it earns a first-class column.
"""

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ModelBase

if TYPE_CHECKING:
    from app.models.research_paper import ResearchPaper


class PaperMetadata(ModelBase):
    __tablename__ = "paper_metadata"

    paper_id: Mapped[UUID] = mapped_column(
        ForeignKey("research_papers.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    doi: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    arxiv_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    abstract: Mapped[str | None] = mapped_column(String, nullable=True)
    citation_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    published_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    extra: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)

    paper: Mapped["ResearchPaper"] = relationship(back_populates="metadata_record")
