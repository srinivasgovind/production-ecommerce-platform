"""App entry point: builds the FastAPI app and plugs in the routers."""

from fastapi import FastAPI

from store.api.health import router as health_router


def create_app() -> FastAPI:
    """App factory: every call builds a fresh app (tests get a clean one each time)."""
    app = FastAPI(title="Store API", version="0.1.0")
    app.include_router(health_router)
    return app


app = create_app()  # what uvicorn runs: `uvicorn store.main:app`
