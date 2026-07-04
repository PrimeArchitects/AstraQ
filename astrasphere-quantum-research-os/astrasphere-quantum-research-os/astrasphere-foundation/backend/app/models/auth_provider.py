"""Links a user to an identity provider they've authenticated with.

A user always has at least a "password" row (once they set a password)
and/or one row per linked OAuth provider (e.g. "google"). This is what
"connected login providers" in Settings reads from, and what a future
provider (GitHub, ORCID — relevant for researchers) plugs into without
schema changes.
"""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class AuthProvider(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "auth_providers"
    __table_args__ = (
        UniqueConstraint("provider", "provider_account_id", name="uq_provider_account"),
        UniqueConstraint("user_id", "provider", name="uq_user_provider"),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # "password" | "google" (extend as new providers are added — plain
    # string rather than a DB enum so adding a provider is a code
    # change, not a migration).
    provider: Mapped[str] = mapped_column(String(32), nullable=False)

    # The provider's stable identifier for this user (e.g. Google's
    # `sub` claim). Null for the "password" provider, which has no
    # external account id.
    provider_account_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user: Mapped["User"] = relationship(back_populates="auth_providers")
