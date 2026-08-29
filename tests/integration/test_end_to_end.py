"""
End-to-end integration test verifying the complete workflow:
Client Upload -> FastAPI -> AnalysisService -> ImageValidator -> Router -> ModelRegistry -> MockAdapter -> EvidenceGenerator -> Response.
"""

import io
import json
from PIL import Image
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def _create_image_file(filename="test.png", size=(200, 200), color=(100, 150, 200)):
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format="PNG")
    buf.seek(0)
    return (filename, buf, "image/png")

def test_full_change_detection_flow():
    # 1. Health check first
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["mock_mode"] is True

    # 2. Upload two images with metadata
    files = [
        ("files", _create_image_file("before_2023.png", color=(0, 200, 0))),
        ("files", _create_image_file("after_2024.png", color=(200, 0, 0)))
    ]
    metadata = json.dumps({
        "t1_date": "2023-01-15",
        "t2_date": "2024-01-15",
        "region": "Area 51"
    })
    data = {
        "query": "Compare these two images and tell me where construction has increased.",
        "metadata": metadata
    }

    response = client.post("/api/v1/analyze", files=files, data=data)
    assert response.status_code == 200
    res = response.json()

    # 3. Assert structured contracts
    assert "request_id" in res
    assert res["request_id"] != "error"
    assert res["analysis_type"] == "CHANGE_DETECTION"
    assert res["model_used"] == "ChangeFormerV6 (mock)"
    assert res["mock"] is True
    assert res["confidence"] is None  # no fabricated confidence
    assert len(res["evidence"]) > 0
    assert res["evidence"][0]["type"] == "change_map"
    assert len(res["evidence"][0]["bounding_boxes"]) > 0

    # 4. Assert execution trace
    trace = res["processing"]["steps"]
    step_names = [s["step"] for s in trace]
    assert "classify" in step_names
    assert "adapter_selected" in step_names
    assert "model_executed" in step_names
    assert "complete" in step_names
