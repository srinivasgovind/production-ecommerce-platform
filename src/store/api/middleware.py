"""Request middleware: a request ID on every log line, plus one access log line per request."""

import re
import time
import uuid

import structlog
from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint

log = structlog.get_logger()

REQUEST_ID_HEADER = "X-Request-ID"
_SAFE_ID = re.compile(r"^[A-Za-z0-9-]{1,64}$")  # letters, digits, dashes; max 64 chars


def _pick_request_id(incoming: str | None) -> str:
    # Reuse the caller's ID (e.g. from the load balancer) so one request has one ID end to end.
    # But never trust it blindly: junk or a 10 KB string would end up in every log line.
    if incoming and _SAFE_ID.match(incoming):
        return incoming
    return uuid.uuid4().hex


async def request_context(request: Request, call_next: RequestResponseEndpoint) -> Response:
    request_id = _pick_request_id(request.headers.get(REQUEST_ID_HEADER))
    structlog.contextvars.clear_contextvars()  # empty this request's backpack first
    structlog.contextvars.bind_contextvars(request_id=request_id)  # every log line now has it

    start = time.perf_counter()
    try:
        response = await call_next(request)  # run the endpoint
    except Exception:
        log.exception("request_failed", method=request.method, path=request.url.path)
        raise  # don't swallow it: FastAPI still turns it into a 500
    duration_ms = round((time.perf_counter() - start) * 1000, 1)

    log.info(
        "request",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration_ms=duration_ms,
    )
    response.headers[REQUEST_ID_HEADER] = request_id  # client/support can quote it
    return response
