"""AstraSphere Quantum Research OS — FastAPI application entrypoint."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import AstraSphereError
from app.core.logging import configure_logging, get_logger
from app.db.redis_client import close_redis
from app.middleware.error_handling import (
    astrasphere_exception_handler,
    unhandled_exception_handler,
)
from app.middleware.request_context import RequestContextMiddleware

settings = get_settings()
configure_logging()
logger = get_logger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("startup", app_env=settings.APP_ENV)
    yield
    await close_redis()
    logger.info("shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        description="AI-powered Quantum Research Operating System — API foundation.",
        docs_url="/docs" if settings.APP_ENV != "production" else None,
        redoc_url="/redoc" if settings.APP_ENV != "production" else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestContextMiddleware)

    app.add_exception_handler(AstraSphereError, astrasphere_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
