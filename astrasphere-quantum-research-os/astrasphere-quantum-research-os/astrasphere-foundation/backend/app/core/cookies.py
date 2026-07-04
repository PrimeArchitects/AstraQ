"""Centralized cookie policy for auth tokens.

One place to set `httponly`/`secure`/`samesite` so every endpoint that
issues or clears auth cookies uses the identical, reviewed policy —
rather than each router hand-rolling `response.set_cookie(...)` calls
that could drift out of sync.
"""

from fastapi import Response

from app.core.config import get_settings
from app.core.csrf import generate_csrf_token

settings = get_settings()


def set_auth_cookies(response: Response, *, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key=settings.ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        domain=settings.COOKIE_DOMAIN,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        domain=settings.COOKIE_DOMAIN,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )
    # Non-httpOnly by design — the frontend must be able to read this
    # and echo it back in the X-CSRF-Token header. See app/core/csrf.py.
    response.set_cookie(
        key=settings.CSRF_COOKIE_NAME,
        value=generate_csrf_token(),
        httponly=False,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        domain=settings.COOKIE_DOMAIN,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )


def clear_auth_cookies(response: Response) -> None:
    for cookie_name in (
        settings.ACCESS_TOKEN_COOKIE_NAME,
        settings.REFRESH_TOKEN_COOKIE_NAME,
        settings.CSRF_COOKIE_NAME,
    ):
        response.delete_cookie(cookie_name, path="/", domain=settings.COOKIE_DOMAIN)
