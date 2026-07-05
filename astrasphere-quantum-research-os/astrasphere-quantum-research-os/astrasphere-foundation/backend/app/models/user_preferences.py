"""One-to-one user preferences: settings-page state that isn't identity.

Split from `User` so identity fields (email, name) and preference
fields (theme, notification toggles) can evolve independently — e.g.
adding a new notification channel never touches the users table.
"""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ModelBase

if TYPE_CHECKING:
    from app.models.user import User


class UserPreferences(ModelBase):
    __tablename__ = "user_preferences"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )

    theme: Mapped[str] = mapped_column(String(16), nullable=False, default="dark")

    # Notification preferences are placeholders in this phase (no
    # notification-sending system exists yet) but the schema is real so
    # the settings UI has something durable to read/write against.
    notify_citations: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notify_comments: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notify_weekly_digest: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user: Mapped["User"] = relationship(back_populates="preferences")
