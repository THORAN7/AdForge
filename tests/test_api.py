from fastapi.testclient import TestClient

from adforge.api import app


def test_root_endpoint() -> None:
    response = TestClient(app).get("/")
    assert response.status_code == 200
    assert "AdForge" in response.text
    assert response.headers["content-type"].startswith("text/html")


def test_health_endpoint() -> None:
    response = TestClient(app).get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
