"""Refresh-token session model.

One row per issued refresh token (i.e. per logged-in device/browser).
Access tokens are short-lived JWTs verified statelessly and never
touch this table; only the longer-lived refresh token is tracked here,
so that "log out this device" / "log out everywhere" and rotation
detection are possible.
"""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class Session(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "sessions"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # SHA-256 hash of the refresh token, never the raw token — mirrors
    # password storage discipline: a DB leak shouldn't hand out usable
    # credentials.
    refresh_token_hash: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )

    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="sessions")

    @property
    def is_active(self) -> bool:
        from datetime import UTC

        now = datetime.now(UTC)
        expires = self.expires_at if self.expires_at.tzinfo else self.expires_at.replace(tzinfo=UTC)
        return self.revoked_at is None and expires > now
