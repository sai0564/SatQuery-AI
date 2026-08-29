"""
API tests for POST /api/v1/analyze.
"""

import io
from PIL import Image
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def _create_image_file(filename="test.png", size=(100, 100)):
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=(0, 128, 255))
    img.save(buf, format="PNG")
    buf.seek(0)
    return (filename, buf, "image/png")

def test_analyze_single_image():
    files = [("files", _create_image_file("sat1.png"))]
    data = {
        "query": "Identify any airports or ports in this scene."
    }

    response = client.post("/api/v1/analyze", files=files, data=data)
    assert response.status_code == 200
    res = response.json()
    assert res["request_id"] != "error"
    assert res["analysis_type"] == "SINGLE_IMAGE_VQA"
    assert res["mock"] is True
    assert res["confidence"] is None
    assert "GeoChat-7B" in res["model_used"]
    assert len(res["errors"]) == 0
    assert res["processing"]["duration_ms"] >= 0

def test_analyze_bi_temporal():
    files = [
        ("files", _create_image_file("date1.png")),
        ("files", _create_image_file("date2.png"))
    ]
    data = {
        "query": "Compare these two dates and find new construction."
    }

    response = client.post("/api/v1/analyze", files=files, data=data)
    assert response.status_code == 200
    res = response.json()
    assert res["analysis_type"] == "CHANGE_DETECTION"
    assert res["mock"] is True
    assert "ChangeFormerV6" in res["model_used"]
    assert len(res["evidence"]) > 0

def test_analyze_optical_sar():
    files = [
        ("files", _create_image_file("opt.png")),
        ("files", _create_image_file("sar.png"))
    ]
    data = {
        "query": "Analyze optical and SAR co-registered channels.",
        "modality": "sar"
    }

    response = client.post("/api/v1/analyze", files=files, data=data)
    assert response.status_code == 200
    res = response.json()
    assert res["analysis_type"] == "OPTICAL_SAR_ANALYSIS"
    assert res["mock"] is True
    assert "BIFOLD-RDNet" in res["model_used"]

def test_analyze_invalid_file_format():
    files = [("files", ("test.txt", io.BytesIO(b"not an image"), "text/plain"))]
    data = {"query": "What is here?"}

    response = client.post("/api/v1/analyze", files=files, data=data)
    assert response.status_code == 200
    res = response.json()
    assert len(res["errors"]) > 0
    assert res["errors"][0]["error_code"] == "UNSUPPORTED_FORMAT"
