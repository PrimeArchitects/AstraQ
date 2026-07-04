"""Authentication endpoints: register, login, logout, token refresh,
email verification, and password reset.

Rate limiting is applied per-IP (via Redis) on every endpoint that
could be brute-forced or abused for enumeration/spam, per
docs/authentication.md's threat model.
"""

import httpx
from fastapi import APIRouter, Request, Response, status

from app.api.deps import AuthServiceDep, Cache, CurrentUser
from app.core.config import get_settings
from app.core.cookies import clear_auth_cookies, set_auth_cookies
from app.core.csrf import verify_csrf
from app.core.exceptions import UnauthorizedError, ValidationError
from app.core.rate_limit import client_ip, enforce_rate_limit
from app.models.user import User
from app.schemas.auth import (
    AuthenticatedUserResponse,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    ResendVerificationRequest,
    ResetPasswordRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


def _user_response(user: User) -> AuthenticatedUserResponse:
    return AuthenticatedUserResponse(
        id=str(user.id),
        email=user.email,
        display_name=user.display_name,
        email_verified=user.email_verified,
    )


@router.post(
    "/register", response_model=AuthenticatedUserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    body: RegisterRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDep,
    redis: Cache,
) -> AuthenticatedUserResponse:
    await enforce_rate_limit(
        redis,
        key=f"ratelimit:register:{client_ip(request)}",
        limit=settings.RATE_LIMIT_REGISTER_PER_MINUTE,
    )
    user = await auth_service.register(
        email=body.email, password=body.password, display_name=body.display_name
    )
    tokens = await auth_service.issue_session(
        user, user_agent=request.headers.get("user-agent"), ip_address=client_ip(request)
    )
    set_auth_cookies(response, access_token=tokens.access_token, refresh_token=tokens.refresh_token)
    return _user_response(user)


@router.post("/login", response_model=AuthenticatedUserResponse)
async def login(
    body: LoginRequest,
    request: Request,
    response: Response,
    auth_service: AuthServiceDep,
    redis: Cache,
) -> AuthenticatedUserResponse:
    await enforce_rate_limit(
        redis,
        key=f"ratelimit:login:{client_ip(request)}",
        limit=settings.RATE_LIMIT_LOGIN_PER_MINUTE,
    )
    user = await auth_service.authenticate(email=body.email, password=body.password)
    tokens = await auth_service.issue_session(
        user, user_agent=request.headers.get("user-agent"), ip_address=client_ip(request)
    )
    set_auth_cookies(response, access_token=tokens.access_token, refresh_token=tokens.refresh_token)
    return _user_response(user)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    request: Request, response: Response, auth_service: AuthServiceDep
) -> MessageResponse:
    verify_csrf(request)
    refresh_token = request.cookies.get(settings.REFRESH_TOKEN_COOKIE_NAME)
    if refresh_token:
        await auth_service.logout(refresh_token)
    clear_auth_cookies(response)
    return MessageResponse(message="Logged out.")


@router.post("/refresh", response_model=MessageResponse)
async def refresh(
    request: Request, response: Response, auth_service: AuthServiceDep
) -> MessageResponse:
    refresh_token = request.cookies.get(settings.REFRESH_TOKEN_COOKIE_NAME)
    if not refresh_token:
        raise UnauthorizedError("No active session.")

    tokens = await auth_service.refresh_session(
        refresh_token, user_agent=request.headers.get("user-agent"), ip_address=client_ip(request)
    )
    set_auth_cookies(response, access_token=tokens.access_token, refresh_token=tokens.refresh_token)
    return MessageResponse(message="Session refreshed.")


@router.get("/verify-email", response_model=MessageResponse)
async def verify_email(token: str, auth_service: AuthServiceDep) -> MessageResponse:
    await auth_service.verify_email(token)
    return MessageResponse(message="Email verified successfully.")


@router.post("/verify-email/resend", response_model=MessageResponse)
async def resend_verification(
    body: ResendVerificationRequest, request: Request, auth_service: AuthServiceDep, redis: Cache
) -> MessageResponse:
    await enforce_rate_limit(
        redis,
        key=f"ratelimit:resend-verify:{client_ip(request)}",
        limit=settings.RATE_LIMIT_PASSWORD_RESET_PER_MINUTE,
    )
    await auth_service.resend_verification(body.email)
    return MessageResponse(
        message="If that email is registered and unverified, a new link has been sent."
    )


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    body: ForgotPasswordRequest, request: Request, auth_service: AuthServiceDep, redis: Cache
) -> MessageResponse:
    await enforce_rate_limit(
        redis,
        key=f"ratelimit:forgot-password:{client_ip(request)}",
        limit=settings.RATE_LIMIT_PASSWORD_RESET_PER_MINUTE,
    )
    await auth_service.request_password_reset(body.email)
    return MessageResponse(message="If that email is registered, a reset link has been sent.")


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    body: ResetPasswordRequest, auth_service: AuthServiceDep
) -> MessageResponse:
    await auth_service.reset_password(body.token, body.new_password)
    return MessageResponse(message="Password reset successfully. Please log in.")


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    body: ChangePasswordRequest,
    request: Request,
    response: Response,
    current_user: CurrentUser,
    auth_service: AuthServiceDep,
) -> MessageResponse:
    verify_csrf(request)
    await auth_service.change_password(
        current_user, current_password=body.current_password, new_password=body.new_password
    )
    clear_auth_cookies(response)
    return MessageResponse(message="Password changed. Please log in again.")


@router.get("/me", response_model=AuthenticatedUserResponse)
async def get_current_session(current_user: CurrentUser) -> AuthenticatedUserResponse:
    """Lightweight identity check — used by the frontend on load to
    determine whether an existing session cookie is still valid."""
    return _user_response(current_user)


# --- Google OAuth ---
#
# Fully implemented against Google's real endpoints, but inert until
# GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET are set (see docs/authentication.md
# "OAuth configuration"). Left unconfigured in this environment since no
# real Google Cloud project/credentials exist here to test against.

_GOOGLE_AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
_GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"  # noqa: S105 (URL, not a password)
_GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


@router.get("/oauth/google/authorize")
async def google_authorize() -> dict[str, str]:
    if not settings.GOOGLE_CLIENT_ID:
        raise ValidationError(
            "Google sign-in isn't configured on this server (missing OAuth credentials)."
        )

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return {"authorize_url": f"{_GOOGLE_AUTHORIZE_URL}?{query}"}


@router.get("/oauth/google/callback", response_model=AuthenticatedUserResponse)
async def google_callback(
    code: str,
    request: Request,
    response: Response,
    auth_service: AuthServiceDep,
) -> AuthenticatedUserResponse:
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise ValidationError("Google sign-in isn't configured on this server.")

    async with httpx.AsyncClient(timeout=10.0) as client:
        token_response = await client.post(
            _GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        if token_response.status_code != 200:
            raise ValidationError("Google sign-in failed. Please try again.")
        google_access_token = token_response.json()["access_token"]

        userinfo_response = await client.get(
            _GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {google_access_token}"},
        )
        if userinfo_response.status_code != 200:
            raise ValidationError("Google sign-in failed. Please try again.")
        profile = userinfo_response.json()

    user = await auth_service.get_or_create_oauth_user(
        provider="google",
        provider_account_id=profile["sub"],
        email=profile["email"],
        display_name=profile.get("name", profile["email"].split("@")[0]),
        avatar_url=profile.get("picture"),
    )
    tokens = await auth_service.issue_session(
        user, user_agent=request.headers.get("user-agent"), ip_address=client_ip(request)
    )
    set_auth_cookies(response, access_token=tokens.access_token, refresh_token=tokens.refresh_token)
    return _user_response(user)
