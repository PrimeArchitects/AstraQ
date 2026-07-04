"""User account model — the source of truth for identity in this system.

Authentication is self-hosted (see docs/authentication.md for why, given
the DB-ownership requirements this project has); this table, not a
third-party identity provider, is where "who is this user" is answered.
"""

from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.auth_provider import AuthProvider
    from app.models.session import Session
    from app.models.user_preferences import UserPreferences


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    # Stored lowercased (enforced in the service layer) so lookups and
    # the uniqueness constraint are case-insensitive without needing a
    # Postgres extension.
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)

    # Nullable: an OAuth-only user (e.g. Google sign-in, never set a
    # password) has no hash to store. Login-by-password checks this is
    # non-null before attempting verification.
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)

    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    institution: Mapped[str | None] = mapped_column(String(255), nullable=True)
    research_interests: Mapped[list[str]] = mapped_column(
        ARRAY(String(80)), nullable=False, default=list
    )
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="UTC")

    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    preferences: Mapped["UserPreferences"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    auth_providers: Mapped[list["AuthProvider"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
