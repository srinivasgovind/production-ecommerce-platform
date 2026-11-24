"""The skeleton's first test: the app starts and /health answers."""

from fastapi.testclient import TestClient

from store.main import create_app


def test_health_returns_ok() -> None:
    client = TestClient(create_app())  # sends fake HTTP requests to the app, no real server or port

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
