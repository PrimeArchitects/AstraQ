"""Placeholder team/workspace model — schema only, no team-specific
business logic (shared folders, permissions, invites) is implemented
in this step."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ModelBase, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.team_member import TeamMember
    from app.models.user import User


class TeamWorkspace(ModelBase, SoftDeleteMixin):
    __tablename__ = "team_workspaces"

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    owner: Mapped["User"] = relationship()
    members: Mapped[list["TeamMember"]] = relationship(
        back_populates="workspace", cascade="all, delete-orphan"
    )
