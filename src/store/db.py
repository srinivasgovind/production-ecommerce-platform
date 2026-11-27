"""Database access: one engine (= connection pool) per app process, created at startup."""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from store.api.health import ReadinessCheck
from store.config import Settings


def create_engine(settings: Settings) -> AsyncEngine:
    """Build the pool. No connection is opened yet: the first query opens one."""
    return create_async_engine(
        settings.database_url,
        pool_size=5,  # connections kept open (size = requests/s x query time; see the pool notes)
        max_overflow=5,  # up to 5 extra during a spike, closed again afterwards
        pool_timeout=2,  # all busy for 2 s -> raise instead of hanging (default is 30 s)
        connect_args={"timeout": 3},  # give up opening a NEW connection after 3 s
    )


def database_check(engine: AsyncEngine) -> ReadinessCheck:
    """Readiness check for /ready: can we borrow a connection and run a trivial query?"""

    async def check() -> None:
        async with engine.connect() as conn:  # borrow from the pool, always given back
            await conn.execute(text("SELECT 1"))

    return check
