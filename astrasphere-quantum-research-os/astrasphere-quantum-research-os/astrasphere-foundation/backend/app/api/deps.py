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
from app.repositories.activity_log_repository import ActivityLogRepository
from app.repositories.ai_job_repository import AIJobRepository
from app.repositories.bookmark_repository import BookmarkRepository
from app.repositories.chat_repository import ChatMessageRepository, ChatSessionRepository
from app.repositories.file_repository import FileRepository
from app.repositories.folder_repository import FolderRepository
from app.repositories.notification_repository import NotificationRepository
from app.repositories.paper_repository import PaperRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.tag_repository import TagRepository
from app.repositories.team_repository import TeamMemberRepository, TeamWorkspaceRepository
from app.repositories.user_repository import UserRepository
from app.services.activity_log_service import ActivityLogService
from app.services.ai_job_service import AIJobService
from app.services.auth_service import AuthService
from app.services.bookmark_service import BookmarkService
from app.services.chat_service import ChatService
from app.services.file_service import FileService
from app.services.folder_service import FolderService
from app.services.notification_service import NotificationService
from app.services.paper_service import PaperService
from app.services.tag_service import TagService
from app.services.team_service import TeamService
from app.services.user_service import UserService

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
Cache = Annotated[Redis, Depends(get_redis)]
VectorStore = Annotated[object, Depends(get_qdrant)]


# --- Repositories ---


def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)


def get_session_repository(db: DbSession) -> SessionRepository:
    return SessionRepository(db)


def get_folder_repository(db: DbSession) -> FolderRepository:
    return FolderRepository(db)


def get_tag_repository(db: DbSession) -> TagRepository:
    return TagRepository(db)


def get_paper_repository(db: DbSession) -> PaperRepository:
    return PaperRepository(db)


def get_bookmark_repository(db: DbSession) -> BookmarkRepository:
    return BookmarkRepository(db)


def get_file_repository(db: DbSession) -> FileRepository:
    return FileRepository(db)


def get_chat_session_repository(db: DbSession) -> ChatSessionRepository:
    return ChatSessionRepository(db)


def get_chat_message_repository(db: DbSession) -> ChatMessageRepository:
    return ChatMessageRepository(db)


def get_notification_repository(db: DbSession) -> NotificationRepository:
    return NotificationRepository(db)


def get_activity_log_repository(db: DbSession) -> ActivityLogRepository:
    return ActivityLogRepository(db)


def get_ai_job_repository(db: DbSession) -> AIJobRepository:
    return AIJobRepository(db)


def get_team_workspace_repository(db: DbSession) -> TeamWorkspaceRepository:
    return TeamWorkspaceRepository(db)


def get_team_member_repository(db: DbSession) -> TeamMemberRepository:
    return TeamMemberRepository(db)


UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
SessionRepo = Annotated[SessionRepository, Depends(get_session_repository)]
FolderRepo = Annotated[FolderRepository, Depends(get_folder_repository)]
TagRepo = Annotated[TagRepository, Depends(get_tag_repository)]
PaperRepo = Annotated[PaperRepository, Depends(get_paper_repository)]
BookmarkRepo = Annotated[BookmarkRepository, Depends(get_bookmark_repository)]
FileRepo = Annotated[FileRepository, Depends(get_file_repository)]
ChatSessionRepo = Annotated[ChatSessionRepository, Depends(get_chat_session_repository)]
ChatMessageRepo = Annotated[ChatMessageRepository, Depends(get_chat_message_repository)]
NotificationRepo = Annotated[NotificationRepository, Depends(get_notification_repository)]
ActivityLogRepo = Annotated[ActivityLogRepository, Depends(get_activity_log_repository)]
AIJobRepo = Annotated[AIJobRepository, Depends(get_ai_job_repository)]
TeamWorkspaceRepo = Annotated[TeamWorkspaceRepository, Depends(get_team_workspace_repository)]
TeamMemberRepo = Annotated[TeamMemberRepository, Depends(get_team_member_repository)]


# --- Services ---


def get_auth_service(
    user_repo: UserRepo,
    session_repo: SessionRepo,
    email_sender: Annotated[EmailSender, Depends(get_email_sender)],
) -> AuthService:
    return AuthService(user_repo, session_repo, email_sender)


def get_user_service(user_repo: UserRepo, session_repo: SessionRepo) -> UserService:
    return UserService(user_repo, session_repo)


def get_folder_service(folder_repo: FolderRepo) -> FolderService:
    return FolderService(folder_repo)


def get_tag_service(tag_repo: TagRepo) -> TagService:
    return TagService(tag_repo)


def get_paper_service(paper_repo: PaperRepo, tag_repo: TagRepo) -> PaperService:
    return PaperService(paper_repo, tag_repo)


def get_bookmark_service(bookmark_repo: BookmarkRepo, paper_repo: PaperRepo) -> BookmarkService:
    return BookmarkService(bookmark_repo, paper_repo)


def get_file_service(file_repo: FileRepo, paper_repo: PaperRepo) -> FileService:
    return FileService(file_repo, paper_repo)


def get_chat_service(
    chat_session_repo: ChatSessionRepo, chat_message_repo: ChatMessageRepo, paper_repo: PaperRepo
) -> ChatService:
    return ChatService(chat_session_repo, chat_message_repo, paper_repo)


def get_notification_service(notification_repo: NotificationRepo) -> NotificationService:
    return NotificationService(notification_repo)


def get_activity_log_service(activity_log_repo: ActivityLogRepo) -> ActivityLogService:
    return ActivityLogService(activity_log_repo)


def get_ai_job_service(ai_job_repo: AIJobRepo) -> AIJobService:
    return AIJobService(ai_job_repo)


def get_team_service(workspace_repo: TeamWorkspaceRepo, member_repo: TeamMemberRepo) -> TeamService:
    return TeamService(workspace_repo, member_repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
FolderServiceDep = Annotated[FolderService, Depends(get_folder_service)]
TagServiceDep = Annotated[TagService, Depends(get_tag_service)]
PaperServiceDep = Annotated[PaperService, Depends(get_paper_service)]
BookmarkServiceDep = Annotated[BookmarkService, Depends(get_bookmark_service)]
FileServiceDep = Annotated[FileService, Depends(get_file_service)]
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
NotificationServiceDep = Annotated[NotificationService, Depends(get_notification_service)]
ActivityLogServiceDep = Annotated[ActivityLogService, Depends(get_activity_log_service)]
AIJobServiceDep = Annotated[AIJobService, Depends(get_ai_job_service)]
TeamServiceDep = Annotated[TeamService, Depends(get_team_service)]


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
