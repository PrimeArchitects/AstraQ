"""
Authentication business logic: registration, login, token issuance/
rotation, email verification, and password reset.

Deliberately generic error messages throughout for anything that could
otherwise leak account existence (login, forgot-password, resend-
verification) — see individual method docstrings for the specific
attack each guards against.
"""

import uuid
from datetime import UTC, datetime, timedelta

from app.core.config import get_settings
from app.core.email import EmailSender
from app.core.exceptions import ConflictError, NotFoundError, UnauthorizedError, ValidationError
from app.core.security import (
    InvalidTokenError,
    TokenPurpose,
    create_access_token,
    create_email_verification_token,
    create_password_reset_token,
    create_refresh_token,
    decode_token,
    fingerprint,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.services.base import BaseService

settings = get_settings()

# A validly-formatted bcrypt hash, generated once at import time, used
# only so verify_password() has something correctly-shaped to compare
# against when short-circuiting a nonexistent-user login attempt (a
# timing-safety measure — see `authenticate()`). Never matches any real
# password.
_DUMMY_HASH = hash_password("timing-safety-placeholder-never-a-real-password")


class TokenPair:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token


class AuthService(BaseService):
    def __init__(
        self,
        user_repo: UserRepository,
        session_repo: SessionRepository,
        email_sender: EmailSender,
    ) -> None:
        self.users = user_repo
        self.sessions = session_repo
        self.email = email_sender

    async def register(self, *, email: str, password: str, display_name: str) -> User:
        normalized_email = email.lower().strip()
        if await self.users.email_exists(normalized_email):
            # Deliberately vague: confirms an *email format* problem
            # would 422 earlier via Pydantic; this only fires for a
            # genuine duplicate, so being explicit here is a considered
            # trade-off (usability) rather than an oversight — unlike
            # login, "this email is taken" doesn't help an attacker
            # authenticate as anyone.
            raise ConflictError("An account with this email already exists.")

        user = User(
            email=normalized_email,
            hashed_password=hash_password(password),
            display_name=display_name.strip(),
            email_verified=False,
        )
        user = await self.users.create(user)
        await self.users.create_preferences(user.id)
        await self.users.add_auth_provider(user.id, provider="password")

        token = create_email_verification_token(user.id, user.email)
        verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        await self.email.send(
            to=user.email,
            subject="Verify your AstraSphere account",
            body=f"Welcome to AstraSphere. Verify your email: {verify_url}",
        )
        return user

    async def authenticate(self, *, email: str, password: str) -> User:
        """Raises UnauthorizedError with an identical message whether the
        email doesn't exist or the password is wrong — distinguishing
        the two lets an attacker enumerate registered emails."""
        user = await self.users.get_by_email(email)
        if user is None or user.hashed_password is None:
            # Run a hash comparison anyway against a dummy hash so the
            # response time doesn't itself leak whether the email exists
            # (a timing side-channel).
            verify_password(password, _DUMMY_HASH)
            raise UnauthorizedError("Incorrect email or password.")

        if not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Incorrect email or password.")

        if not user.is_active:
            raise UnauthorizedError("This account has been deactivated.")

        return user

    async def issue_session(
        self, user: User, *, user_agent: str | None, ip_address: str | None
    ) -> TokenPair:
        session_id = uuid.uuid4()
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id, session_id)
        expires_at = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        await self.sessions.create_session(
            session_id=session_id,
            user_id=user.id,
            raw_refresh_token=refresh_token,
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address,
        )
        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def refresh_session(
        self, raw_refresh_token: str, *, user_agent: str | None, ip_address: str | None
    ) -> TokenPair:
        """Rotates the refresh token on every use: the old one is revoked
        and a new one issued, so a leaked-and-reused refresh token is
        usable exactly once before the legitimate session breaks (a
        detectable signal of compromise, even without active alerting)."""
        try:
            payload = decode_token(raw_refresh_token, TokenPurpose.REFRESH)
        except InvalidTokenError as exc:
            raise UnauthorizedError("Session expired. Please log in again.") from exc

        session_record = await self.sessions.get_by_raw_token(raw_refresh_token)
        if session_record is None or not session_record.is_active:
            raise UnauthorizedError("Session expired. Please log in again.")

        user = await self.users.get(uuid.UUID(payload["sub"]))
        if user is None or not user.is_active:
            raise UnauthorizedError("Session expired. Please log in again.")

        await self.sessions.revoke(session_record)
        return await self.issue_session(user, user_agent=user_agent, ip_address=ip_address)

    async def logout(self, raw_refresh_token: str) -> None:
        session_record = await self.sessions.get_by_raw_token(raw_refresh_token)
        if session_record is not None and session_record.is_active:
            await self.sessions.revoke(session_record)

    async def verify_email(self, token: str) -> User:
        try:
            payload = decode_token(token, TokenPurpose.EMAIL_VERIFICATION)
        except InvalidTokenError as exc:
            raise ValidationError(
                "This verification link is invalid or has expired. Request a new one."
            ) from exc

        user = await self.users.get(uuid.UUID(payload["sub"]))
        if user is None:
            raise NotFoundError("Account not found.")
        if user.email != payload.get("email"):
            # Email was changed after the link was issued — stale token.
            raise ValidationError("This verification link is no longer valid.")

        user.email_verified = True
        return user

    async def resend_verification(self, email: str) -> None:
        user = await self.users.get_by_email(email)
        if user is None or user.email_verified:
            return  # Silent no-op: don't reveal account existence/state.

        token = create_email_verification_token(user.id, user.email)
        verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        await self.email.send(
            to=user.email,
            subject="Verify your AstraSphere account",
            body=f"Verify your email: {verify_url}",
        )

    async def request_password_reset(self, email: str) -> None:
        user = await self.users.get_by_email(email)
        if user is None or user.hashed_password is None:
            return  # Silent no-op: don't reveal account existence.

        token = create_password_reset_token(user.id, fingerprint(user.hashed_password))
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        await self.email.send(
            to=user.email,
            subject="Reset your AstraSphere password",
            body=f"Reset your password: {reset_url}",
        )

    async def reset_password(self, token: str, new_password: str) -> User:
        try:
            payload = decode_token(token, TokenPurpose.PASSWORD_RESET)
        except InvalidTokenError as exc:
            raise ValidationError(
                "This password reset link is invalid or has expired. Request a new one."
            ) from exc

        user = await self.users.get(uuid.UUID(payload["sub"]))
        if user is None or user.hashed_password is None:
            raise NotFoundError("Account not found.")

        if payload.get("pwfp") != fingerprint(user.hashed_password):
            # Password already changed since this token was issued
            # (including by a prior use of this exact token) — reject.
            raise ValidationError("This password reset link has already been used or is stale.")

        user.hashed_password = hash_password(new_password)
        await self.sessions.revoke_all_for_user(user.id)
        return user

    async def change_password(
        self, user: User, *, current_password: str, new_password: str
    ) -> None:
        if user.hashed_password is None or not verify_password(
            current_password, user.hashed_password
        ):
            raise UnauthorizedError("Current password is incorrect.")

        user.hashed_password = hash_password(new_password)
        await self.sessions.revoke_all_for_user(user.id)

    async def get_or_create_oauth_user(
        self,
        *,
        provider: str,
        provider_account_id: str,
        email: str,
        display_name: str,
        avatar_url: str | None,
    ) -> User:
        """Google (and future OAuth providers) verify email ownership
        themselves, so an account created/linked this way is marked
        `email_verified=True` immediately — no separate verification
        email needed."""
        existing_link_user = await self.users.get_by_oauth_account(provider, provider_account_id)
        if existing_link_user is not None:
            return existing_link_user

        user = await self.users.get_by_email(email)
        if user is None:
            user = User(
                email=email.lower().strip(),
                hashed_password=None,
                display_name=display_name,
                avatar_url=avatar_url,
                email_verified=True,
            )
            user = await self.users.create(user)
            await self.users.create_preferences(user.id)
        else:
            user.email_verified = True

        existing_provider = await self.users.get_auth_provider(user.id, provider)
        if existing_provider is None:
            await self.users.add_auth_provider(user.id, provider, provider_account_id)

        return user
