"""App entry point: builds the FastAPI app and plugs in the routers."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from store.api.health import router as health_router
from store.api.middleware import request_context
from store.config import Settings, get_settings
from store.db import create_engine, database_check
from store.logs import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup (before yield) and shutdown (after yield) of one app process."""
    engine = create_engine(app.state.settings)
    app.state.engine = engine
    app.state.readiness_checks["database"] = database_check(engine)
    try:
        yield  # the app serves requests while paused here
    finally:
        await engine.dispose()  # shutdown (even after an error): close every pooled connection


def create_app(settings: Settings | None = None) -> FastAPI:
    """App factory: every call builds a fresh app. Tests can pass their own Settings."""
    settings = settings or get_settings()  # bad config → ValidationError HERE, before any traffic
    configure_logging(settings.log_level, settings.log_format)

    app = FastAPI(title="Store API", version="0.1.0", lifespan=lifespan)
    app.state.settings = settings  # one place to reach config at run time
    app.state.readiness_checks = {}  # name → async check; lifespan adds "database"
    app.middleware("http")(request_context)  # wraps EVERY request
    app.include_router(health_router)
    return app


app = create_app()  # what uvicorn runs: `uvicorn store.main:app`
