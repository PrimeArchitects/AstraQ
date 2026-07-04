"""
CSRF protection via the double-submit cookie pattern.

Access/refresh tokens live in httpOnly cookies (so JS can't read them,
protecting against XSS-driven token theft), which means the browser
attaches them automatically — including to a forged cross-site request.
To close that gap: on login, a second, *non*-httpOnly `csrf_token`
cookie is also set. The frontend reads it and echoes it back in an
`X-CSRF-Token` header on every mutating request; a forged cross-site
request can trigger the cookie but can't read it to set the header, so
it fails verification.

Bearer-token clients (mobile apps, service-to-service calls) are exempt
— they don't rely on ambient cookie authority, so CSRF doesn't apply to
them.
"""

import secrets

from fastapi import Request

from app.core.config import get_settings
from app.core.exceptions import ForbiddenError

settings = get_settings()

CSRF_HEADER_NAME = "X-CSRF-Token"
_SAFE_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def verify_csrf(request: Request) -> None:
    """
    Call from mutating routes that authenticate via cookie. Skips
    verification for safe (read-only) methods and for requests
    authenticated via `Authorization: Bearer` rather than cookies.
    """
    if request.method in _SAFE_METHODS:
        return
    if request.headers.get("authorization", "").lower().startswith("bearer "):
        return

    cookie_token = request.cookies.get(settings.CSRF_COOKIE_NAME)
    header_token = request.headers.get(CSRF_HEADER_NAME)

    if (
        not cookie_token
        or not header_token
        or not secrets.compare_digest(cookie_token, header_token)
    ):
        raise ForbiddenError("CSRF token missing or invalid.")
