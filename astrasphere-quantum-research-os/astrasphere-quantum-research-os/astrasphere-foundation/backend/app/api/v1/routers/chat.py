"""Chat session/message endpoints. Persistence only — no AI generation
is wired up here (out of scope for this step)."""

from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps import ChatServiceDep, CurrentUser
from app.schemas.chat import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatSessionCreate,
    ChatSessionDetailResponse,
    ChatSessionResponse,
    ChatSessionUpdate,
)

router = APIRouter(prefix="/chat/sessions", tags=["chat"])


@router.get("", response_model=list[ChatSessionResponse])
async def list_sessions(
    current_user: CurrentUser, service: ChatServiceDep
) -> list[ChatSessionResponse]:
    sessions = await service.list_sessions(current_user)
    return [ChatSessionResponse.model_validate(s) for s in sessions]


@router.post("", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    payload: ChatSessionCreate, current_user: CurrentUser, service: ChatServiceDep
) -> ChatSessionResponse:
    session = await service.create_session(current_user, payload)
    return ChatSessionResponse.model_validate(session)


@router.get("/{session_id}", response_model=ChatSessionDetailResponse)
async def get_session(
    session_id: UUID, current_user: CurrentUser, service: ChatServiceDep
) -> ChatSessionDetailResponse:
    session = await service.get_owned(current_user, session_id)
    return ChatSessionDetailResponse.model_validate(session)


@router.patch("/{session_id}", response_model=ChatSessionResponse)
async def update_session(
    session_id: UUID,
    payload: ChatSessionUpdate,
    current_user: CurrentUser,
    service: ChatServiceDep,
) -> ChatSessionResponse:
    session = await service.update_session(current_user, session_id, payload)
    return ChatSessionResponse.model_validate(session)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: UUID, current_user: CurrentUser, service: ChatServiceDep
) -> None:
    await service.delete_session(current_user, session_id)


@router.post(
    "/{session_id}/messages",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_message(
    session_id: UUID,
    payload: ChatMessageCreate,
    current_user: CurrentUser,
    service: ChatServiceDep,
) -> ChatMessageResponse:
    message = await service.add_message(current_user, session_id, payload)
    return ChatMessageResponse.model_validate(message)
