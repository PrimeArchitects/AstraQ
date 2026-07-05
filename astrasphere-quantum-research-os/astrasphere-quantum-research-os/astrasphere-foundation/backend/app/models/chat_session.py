"""A conversation thread, optionally scoped to a specific paper.

No AI logic lives here (out of scope for this step) — this is purely
the persistence shape a future AI-assistant feature will read/write.
"""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ModelBase, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.chat_message import ChatMessage
    from app.models.research_paper import ResearchPaper
    from app.models.user import User


class ChatSession(ModelBase, SoftDeleteMixin):
    __tablename__ = "chat_sessions"

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    paper_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("research_papers.id", ondelete="SET NULL"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, default="New conversation")

    owner: Mapped["User"] = relationship()
    paper: Mapped["ResearchPaper | None"] = relationship(back_populates="chat_sessions")
    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at"
    )
