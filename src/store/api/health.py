"""Liveness (/health) and readiness (/ready) endpoints for load balancers and orchestrators."""

import asyncio
from collections.abc import Awaitable, Callable

import structlog
from fastapi import APIRouter, Request, Response, status

log = structlog.get_logger()
router = APIRouter(tags=["health"])

ReadinessCheck = Callable[[], Awaitable[None]]  # an async function that raises if not usable
CHECK_TIMEOUT_S = 1.0  # a hanging dependency must not hang the readiness probe


@router.get("/health")
async def health() -> dict[str, str]:
    # Liveness: NO dependency calls on purpose. If this checked the DB, a slow DB would make
    # every container fail at once and get restarted together (errors doc, topic 16).
    return {"status": "ok"}


async def _run_check(name: str, check: ReadinessCheck) -> tuple[str, str]:
    try:
        await asyncio.wait_for(check(), timeout=CHECK_TIMEOUT_S)
        return name, "ok"
    except Exception as exc:  # timeout or any error = not ready (but never crash the probe)
        log.warning("readiness_check_failed", check=name, error=type(exc).__name__)
        return name, "failed"


@router.get("/ready")
async def ready(request: Request, response: Response) -> dict[str, str | dict[str, str]]:
    # Readiness: can we serve traffic now? Failing = "stop sending me requests", not "kill me".
    checks: dict[str, ReadinessCheck] = request.app.state.readiness_checks
    results = dict(await asyncio.gather(*(_run_check(n, c) for n, c in checks.items())))

    if all(result == "ok" for result in results.values()):
        return {"status": "ready", "checks": results}
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE  # LB: take me out of rotation
    return {"status": "not_ready", "checks": results}
