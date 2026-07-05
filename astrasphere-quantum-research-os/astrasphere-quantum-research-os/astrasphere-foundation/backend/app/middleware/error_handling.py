"""Translates domain exceptions into consistent JSON error responses.

Registered on the FastAPI app via `add_exception_handler`, not as
middleware, since exception handlers need typed dispatch on exception
class. Keeping this centralized means routers never write
try/except-to-HTTPException boilerplate.
"""

import structlog
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.exceptions import (
    AstraSphereError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
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
    RateLimitError: status.HTTP_429_TOO_MANY_REQUESTS,
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


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Reshapes FastAPI's default validation-error body (a bare `detail`
    list) into the same `{"error", "detail"}` envelope every other
    error uses, so API consumers never need two code paths."""
    first_error = exc.errors()[0] if exc.errors() else None
    detail = first_error["msg"] if first_error else "Invalid request."
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "ValidationError", "detail": detail, "errors": exc.errors()},
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """A unique-constraint or foreign-key violation that reached the DB
    without being caught by a service-level pre-check (e.g. a race
    between two concurrent requests). Reported as a conflict rather
    than a raw 500 — but the underlying DB error text is logged only,
    never sent to the client, since it can include column/constraint
    names that are internal implementation detail."""
    logger.warning("database_integrity_error", error=str(exc.orig))
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "ConflictError",
            "detail": "This operation conflicts with existing data.",
        },
    )


async def database_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Catch-all for any other database error (connection loss, timeout,
    query error) — never leak driver/SQL internals to the client."""
    logger.error("database_error", error=str(exc), exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "DatabaseError",
            "detail": "A database error occurred. Please try again.",
        },
    )
