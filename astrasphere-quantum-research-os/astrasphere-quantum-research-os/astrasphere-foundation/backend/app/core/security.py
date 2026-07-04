"""
Password hashing and JWT issuance/verification.

Every authentication-security decision in the codebase should route
through here rather than being reimplemented per-endpoint: one hashing
scheme, one token format, one place to rotate `SECRET_KEY` and have it
take effect everywhere.
"""

import uuid
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

# bcrypt: deliberately slow, salted automatically per-hash, industry
# standard for password storage. Cost factor 12 balances brute-force
# resistance against login latency on commodity hardware.
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def hash_password(plain_password: str) -> str:
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)


class TokenPurpose(StrEnum):
    """Every JWT carries a `purpose` claim so a token minted for one
    action (e.g. email verification) can never be replayed for another
    (e.g. as an access token) even if an attacker captures it."""

    ACCESS = "access"
    REFRESH = "refresh"
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"  # noqa: S105 (token purpose label, not a password)


class InvalidTokenError(Exception):
    """Raised for any malformed, expired, or wrong-purpose token."""


def _create_token(
    subject: uuid.UUID,
    purpose: TokenPurpose,
    expires_delta: timedelta,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "purpose": purpose.value,
        "iat": now,
        "exp": now + expires_delta,
        "jti": str(uuid.uuid4()),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: uuid.UUID) -> str:
    return _create_token(
        user_id, TokenPurpose.ACCESS, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(user_id: uuid.UUID, session_id: uuid.UUID) -> str:
    return _create_token(
        user_id,
        TokenPurpose.REFRESH,
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        extra_claims={"sid": str(session_id)},
    )


def create_email_verification_token(user_id: uuid.UUID, email: str) -> str:
    return _create_token(
        user_id,
        TokenPurpose.EMAIL_VERIFICATION,
        timedelta(hours=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS),
        extra_claims={"email": email},
    )


def create_password_reset_token(user_id: uuid.UUID, password_hash_fingerprint: str) -> str:
    """
    `password_hash_fingerprint` (a short hash of the current password
    hash) is embedded so a reset token is automatically invalidated the
    moment the password actually changes — including by a previous use
    of this same token — without needing a token-blocklist table.
    """
    return _create_token(
        user_id,
        TokenPurpose.PASSWORD_RESET,
        timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES),
        extra_claims={"pwfp": password_hash_fingerprint},
    )


def decode_token(token: str, expected_purpose: TokenPurpose) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError as exc:
        raise InvalidTokenError(
            "Token is malformed, expired, or has an invalid signature."
        ) from exc

    if payload.get("purpose") != expected_purpose.value:
        raise InvalidTokenError("Token cannot be used for this operation.")

    return payload


def fingerprint(value: str) -> str:
    """Short, non-reversible fingerprint of a password hash, for embedding in reset tokens."""
    import hashlib

    return hashlib.sha256(value.encode()).hexdigest()[:16]
