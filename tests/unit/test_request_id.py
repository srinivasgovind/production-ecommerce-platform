"""Request-ID middleware: every response gets an ID; safe incoming IDs reused, unsafe replaced."""

import re

import pytest
from fastapi.testclient import TestClient
from structlog.testing import capture_logs

from store.main import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())  # fresh app per test


def test_generates_request_id_when_none_sent(client: TestClient) -> None:
    response = client.get("/health")

    assert re.fullmatch(r"[0-9a-f]{32}", response.headers["X-Request-ID"])  # uuid4().hex


def test_reuses_safe_incoming_request_id(client: TestClient) -> None:
    response = client.get("/health", headers={"X-Request-ID": "support-ticket-42"})

    assert response.headers["X-Request-ID"] == "support-ticket-42"


def test_replaces_unsafe_incoming_request_id(client: TestClient) -> None:
    unsafe = "<script>alert(1)</script>"

    response = client.get("/health", headers={"X-Request-ID": unsafe})

    assert response.headers["X-Request-ID"] != unsafe
    assert re.fullmatch(r"[0-9a-f]{32}", response.headers["X-Request-ID"])


def test_replaces_too_long_request_id(client: TestClient) -> None:
    response = client.get("/health", headers={"X-Request-ID": "a" * 65})  # limit is 64

    assert response.headers["X-Request-ID"] != "a" * 65


def test_logs_one_access_line_per_request(client: TestClient) -> None:
    with capture_logs() as logs:  # structlog test helper: collects log events as dicts
        client.get("/health")

    access = [entry for entry in logs if entry["event"] == "request"]
    assert len(access) == 1
    assert access[0]["status"] == 200
    assert access[0]["path"] == "/health"
