"""App entry point: builds the FastAPI app and plugs in the routers."""

from fastapi import FastAPI

from store.api.health import router as health_router
from store.api.middleware import request_context
from store.config import Settings, get_settings
from store.logs import configure_logging


def create_app(settings: Settings | None = None) -> FastAPI:
    """App factory: every call builds a fresh app. Tests can pass their own Settings."""
    settings = settings or get_settings()  # bad config → ValidationError HERE, before any traffic
    configure_logging(settings.log_level, settings.log_format)

    app = FastAPI(title="Store API", version="0.1.0")
    app.state.settings = settings  # one place to reach config at run time
    app.state.readiness_checks = {}  # name → async check; step 3 adds "database"
    app.middleware("http")(request_context)  # wraps EVERY request
    app.include_router(health_router)
    return app


app = create_app()  # what uvicorn runs: `uvicorn store.main:app`
