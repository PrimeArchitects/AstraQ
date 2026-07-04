"""Shared FastAPI dependencies: DB/cache/vector-store handles, auth, and
per-request service instances."""

import uuid
from typing import Annotated

from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.email import EmailSender, get_email_sender
from app.core.exceptions import UnauthorizedError
from app.core.security import InvalidTokenError, TokenPurpose, decode_token
from app.db.qdrant_client import get_qdrant
from app.db.redis_client import get_redis
from app.db.session import get_db_session
from app.models.user import User
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
Cache = Annotated[Redis, Depends(get_redis)]
VectorStore = Annotated[object, Depends(get_qdrant)]


def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)


def get_session_repository(db: DbSession) -> SessionRepository:
    return SessionRepository(db)


UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
SessionRepo = Annotated[SessionRepository, Depends(get_session_repository)]


def get_auth_service(
    user_repo: UserRepo,
    session_repo: SessionRepo,
    email_sender: Annotated[EmailSender, Depends(get_email_sender)],
) -> AuthService:
    return AuthService(user_repo, session_repo, email_sender)


def get_user_service(user_repo: UserRepo, session_repo: SessionRepo) -> UserService:
    return UserService(user_repo, session_repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def _extract_access_token(request: Request) -> str | None:
    """Accepts either the httpOnly cookie (browser clients) or a Bearer
    header (API/mobile clients) — the two supported ways to authenticate."""
    settings = get_settings()
    cookie_token = request.cookies.get(settings.ACCESS_TOKEN_COOKIE_NAME)
    if cookie_token:
        return cookie_token

    auth_header = request.headers.get("authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:]

    return None


async def get_current_user(request: Request, user_repo: UserRepo) -> User:
    token = _extract_access_token(request)
    if token is None:
        raise UnauthorizedError("Authentication required.")

    try:
        payload = decode_token(token, TokenPurpose.ACCESS)
    except InvalidTokenError as exc:
        raise UnauthorizedError("Session expired. Please log in again.") from exc

    user = await user_repo.get(uuid.UUID(payload["sub"]))
    if user is None or not user.is_active:
        raise UnauthorizedError("Session expired. Please log in again.")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
