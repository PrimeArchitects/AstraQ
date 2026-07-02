"""AstraSphere Quantum Research OS — FastAPI application entrypoint."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.services.qdrant_client import ensure_collection

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup/shutdown hooks."""
    logger.info("startup.begin", environment=settings.environment)
    try:
        await ensure_collection()
        logger.info("qdrant.collection_ready", collection=settings.qdrant_collection)
    except Exception as exc:  # pragma: no cover - defensive startup logging
        logger.warning("qdrant.collection_setup_failed", error=str(exc))
    yield
    logger.info("shutdown.complete")


app = FastAPI(
    title=settings.project_name,
    description="Backend API for the AstraSphere Quantum Research OS platform.",
    version="0.1.0",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url=f"{settings.api_v1_prefix}/docs",
    redoc_url=f"{settings.api_v1_prefix}/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler that logs unexpected errors without leaking internals."""
    logger.error("unhandled_exception", path=str(request.url), error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["root"], summary="API root")
async def root() -> dict[str, str]:
    return {
        "service": settings.project_name,
        "status": "online",
        "docs": f"{settings.api_v1_prefix}/docs",
    }
