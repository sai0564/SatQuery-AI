# Integration tests for FastAPI endpoints.
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["health"] == "/api/v1/health"

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "GeoChat-7B" in data["models_available"]
    assert "ChangeFormerV6" in data["models_available"]
    assert "BIFOLD-RDNet" in data["models_available"]

def test_analyze_single_image():
    payload = {
        "image": "base64_or_url_string",
        "query": "Identify runways and hangars."
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["confidence"] > 0
    assert len(data["execution_trace"]) > 0

def test_analyze_bitemporal():
    payload = {
        "image_t1": "t1_data",
        "image_t2": "t2_data",
        "query": "What changed between T1 and T2?"
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "change_detection" in data["evidence"]
    assert data["metadata"]["primary_model"] == "ChangeFormerV6"
