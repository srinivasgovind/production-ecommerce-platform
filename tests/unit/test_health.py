"""Liveness always answers; readiness reflects its dependency checks (503 when any fails)."""

import asyncio

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from store.api import health as health_module
from store.main import create_app


@pytest.fixture
def app() -> FastAPI:
    return create_app()


async def ok_check() -> None:
    return None


async def broken_check() -> None:
    raise ConnectionError("db down")


async def hanging_check() -> None:
    await asyncio.sleep(10)  # never answers in time


def test_health_returns_ok(app: FastAPI) -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_with_no_checks_is_ready(app: FastAPI) -> None:
    response = TestClient(app).get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "checks": {}}


def test_ready_returns_503_when_a_check_fails(app: FastAPI) -> None:
    app.state.readiness_checks = {"database": broken_check, "cache": ok_check}

    response = TestClient(app).get("/ready")

    assert response.status_code == 503
    assert response.json()["checks"] == {"database": "failed", "cache": "ok"}


def test_ready_times_out_a_hanging_check(app: FastAPI, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(health_module, "CHECK_TIMEOUT_S", 0.05)  # keep the test fast
    app.state.readiness_checks = {"database": hanging_check}

    response = TestClient(app).get("/ready")

    assert response.status_code == 503
    assert response.json()["checks"] == {"database": "failed"}


def test_health_stays_ok_when_dependencies_fail(app: FastAPI) -> None:
    app.state.readiness_checks = {"database": broken_check}

    assert TestClient(app).get("/health").status_code == 200  # liveness ignores dependencies
