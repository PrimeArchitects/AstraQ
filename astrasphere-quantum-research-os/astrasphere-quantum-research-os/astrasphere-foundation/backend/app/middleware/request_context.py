"""Request-scoped middleware: correlation IDs and access logging.

Implemented as pure ASGI (not Starlette's `BaseHTTPMiddleware`)
deliberately: `BaseHTTPMiddleware` runs the downstream app in a child
task spawned via an anyio task group, which is known to conflict with
libraries that use raw asyncio primitives directly — redis-py's async
client among them — producing intermittent "Future attached to a
different loop" errors. Pure ASGI middleware runs in the same task as
the request, avoiding the class of bug entirely.
"""

import time
import uuid
from collections.abc import MutableMapping
from typing import Any

import structlog
from starlette.types import ASGIApp, Receive, Scope, Send

logger = structlog.get_logger("http.access")


class RequestContextMiddleware:
    """Attaches a request ID to every request/response and logs access lines.

    The request ID is echoed back in the `X-Request-ID` header so clients
    and logs can be correlated end to end.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        request_id = headers.get(b"x-request-id", b"").decode() or str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(request_id=request_id)

        start = time.perf_counter()
        status_code = 500

        async def send_wrapper(message: MutableMapping[str, Any]) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                headers_list = message.setdefault("headers", [])
                headers_list.append((b"x-request-id", request_id.encode()))
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.info(
                "request_completed",
                method=scope.get("method"),
                path=scope.get("path"),
                status_code=status_code,
                duration_ms=round(duration_ms, 2),
            )
            structlog.contextvars.clear_contextvars()
