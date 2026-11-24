"""Health endpoint: lets load balancers and Docker ask "is this process alive?"."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    # No database call on purpose: "alive" must not fail just because the DB is slow.
    # A separate readiness check (S0 step 2) will check the DB.
    return {"status": "ok"}
