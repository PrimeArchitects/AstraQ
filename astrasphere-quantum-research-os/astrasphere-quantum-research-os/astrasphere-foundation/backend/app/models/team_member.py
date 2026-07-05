"""Placeholder membership row linking a user to a team workspace with
a role. Role enforcement (who can invite/remove/edit) is future work;
this step only establishes the schema."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ModelBase

if TYPE_CHECKING:
    from app.models.team_workspace import TeamWorkspace
    from app.models.user import User

TEAM_MEMBER_ROLES = ("owner", "admin", "member")


class TeamMember(ModelBase):
    __tablename__ = "team_members"
    __table_args__ = (
        UniqueConstraint("workspace_id", "user_id", name="uq_team_member_workspace_user"),
    )

    workspace_id: Mapped[UUID] = mapped_column(
        ForeignKey("team_workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(16), nullable=False, default="member")

    workspace: Mapped["TeamWorkspace"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship()
