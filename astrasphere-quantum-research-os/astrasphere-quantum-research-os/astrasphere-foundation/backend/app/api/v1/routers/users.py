"""Authenticated user-profile, preferences, and account-management endpoints.

Every route here requires `CurrentUser` — there is no public read
access to profile data in this API.
"""

from fastapi import APIRouter, Request, status

from app.api.deps import CurrentUser, UserServiceDep
from app.core.csrf import verify_csrf
from app.schemas.user import (
    AccountDeleteRequest,
    AuthProviderResponse,
    UserPreferencesResponse,
    UserPreferencesUpdateRequest,
    UserProfileResponse,
    UserProfileUpdateRequest,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(current_user: CurrentUser) -> UserProfileResponse:
    return UserProfileResponse.model_validate(current_user)


@router.patch("/me", response_model=UserProfileResponse)
async def update_my_profile(
    body: UserProfileUpdateRequest,
    request: Request,
    current_user: CurrentUser,
    user_service: UserServiceDep,
) -> UserProfileResponse:
    verify_csrf(request)
    updated = await user_service.update_profile(current_user, body)
    return UserProfileResponse.model_validate(updated)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(
    body: AccountDeleteRequest,
    request: Request,
    current_user: CurrentUser,
    user_service: UserServiceDep,
) -> None:
    verify_csrf(request)
    await user_service.delete_account(current_user, password=body.password, confirm=body.confirm)


@router.get("/me/preferences", response_model=UserPreferencesResponse)
async def get_my_preferences(
    current_user: CurrentUser, user_service: UserServiceDep
) -> UserPreferencesResponse:
    prefs = await user_service.get_preferences(current_user)
    return UserPreferencesResponse.model_validate(prefs)


@router.patch("/me/preferences", response_model=UserPreferencesResponse)
async def update_my_preferences(
    body: UserPreferencesUpdateRequest,
    request: Request,
    current_user: CurrentUser,
    user_service: UserServiceDep,
) -> UserPreferencesResponse:
    verify_csrf(request)
    prefs = await user_service.update_preferences(current_user, body)
    return UserPreferencesResponse.model_validate(prefs)


@router.get("/me/auth-providers", response_model=list[AuthProviderResponse])
async def list_my_auth_providers(
    current_user: CurrentUser, user_service: UserServiceDep
) -> list[AuthProviderResponse]:
    providers = await user_service.list_auth_providers(current_user)
    return [AuthProviderResponse.model_validate(p) for p in providers]
