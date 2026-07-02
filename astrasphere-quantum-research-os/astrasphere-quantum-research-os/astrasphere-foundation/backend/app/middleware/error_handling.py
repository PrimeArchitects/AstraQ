"""Translates domain exceptions into consistent JSON error responses.

Registered on the FastAPI app via `add_exception_handler`, not as
middleware, since exception handlers need typed dispatch on exception
class. Keeping this centralized means routers never write
try/except-to-HTTPException boilerplate.
"""

import structlog
from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AstraSphereError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)

logger = structlog.get_logger("error_handling")

_STATUS_MAP: dict[type[AstraSphereError], int] = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    ConflictError: status.HTTP_409_CONFLICT,
    ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    UnauthorizedError: status.HTTP_401_UNAUTHORIZED,
    ForbiddenError: status.HTTP_403_FORBIDDEN,
}


async def astrasphere_exception_handler(request: Request, exc: AstraSphereError) -> JSONResponse:
    status_code = _STATUS_MAP.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
    if status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error("unhandled_domain_error", error=str(exc), exc_info=exc)
    return JSONResponse(
        status_code=status_code,
        content={"error": exc.__class__.__name__, "detail": str(exc)},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("unhandled_exception", error=str(exc), exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "InternalServerError", "detail": "An unexpected error occurred."},
    )
