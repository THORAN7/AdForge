from fastapi.testclient import TestClient

from adforge.api import app


def test_root_endpoint() -> None:
    response = TestClient(app).get("/")
    assert response.status_code == 200
    assert "AdForge" in response.text
    assert response.headers["content-type"].startswith("text/html")
    assert "Phase 1 is active" not in response.text
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert "Content-Security-Policy" in response.headers


def test_packaged_static_asset_is_served() -> None:
    response = TestClient(app).get("/static/index.html")
    assert response.status_code == 200
    assert "AdForge" in response.text


def test_health_endpoint() -> None:
    response = TestClient(app).get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_invalid_generate_request_has_consistent_error_shape() -> None:
    response = TestClient(app).post("/api/generate", json={})
    assert response.status_code == 422
    assert set(response.json()) == {"error", "message", "details"}


def test_generate_returns_consistent_not_implemented_error() -> None:
    payload = {
        "product": {
            "name": "Focus Lamp",
            "category": "lighting",
            "key_features": ["adjustable", "portable", "USB-C"],
            "unique_selling_point": "Flexible workspace light",
            "brand_name": "Northstar",
            "brand_tone": "trustworthy",
        },
        "audiences": [{"preset": "gen_z_students"}],
    }
    response = TestClient(app).post("/api/generate", json=payload)
    assert response.status_code == 501
    assert response.json()["error"] == "generation_not_implemented"


def test_request_size_limit_has_consistent_error_shape() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/generate",
        content=b"x",
        headers={"content-length": str(6 * 1024 * 1024)},
    )
    assert response.status_code == 413
    assert response.json()["error"] == "request_too_large"
