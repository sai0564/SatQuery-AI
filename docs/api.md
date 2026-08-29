# SatQuery AI — API Specification

## Base URL
`/api/v1`

---

## Endpoints

### 1. Health Check
`GET /api/v1/health`

Returns system operational status, mock mode indicator, and registered models.

#### Response (200 OK)
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "mock_mode": true,
  "models_registered": [
    "GeoChat-7B (mock)",
    "ChangeFormerV6 (mock)",
    "BIFOLD-RDNet (mock)"
  ],
  "capabilities": [
    "SINGLE_IMAGE_VQA",
    "IMAGE_DESCRIPTION",
    "CHANGE_DETECTION",
    "BI_TEMPORAL_ANALYSIS",
    "OPTICAL_SAR_ANALYSIS"
  ]
}
```

---

### 2. Analyze Imagery
`POST /api/v1/analyze`

Primary multimodal image analysis endpoint. Accepts multipart form data.

#### Request Parameters (Multipart Form-Data)

| Parameter | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `files` | Binary List | Yes | One or more satellite image files (JPEG, PNG, TIFF) |
| `query` | String | No | Question or instruction (default: `"Describe this image."`) |
| `modality` | String | No | Sensor modality hint (`optical`, `sar`) |
| `metadata` | JSON String | No | Optional metadata (e.g. `{"t1_date": "2023-01-01", "t2_date": "2024-01-01"}`) |

#### Response (200 OK)
```json
{
  "request_id": "9a3f2b8c-...",
  "analysis_type": "CHANGE_DETECTION",
  "answer": "Detected significant spatial changes covering ~12.5% of the area.",
  "model_used": "ChangeFormerV6 (mock)",
  "confidence": null,
  "mock": true,
  "evidence": [
    {
      "type": "change_map",
      "description": "Simulated change map showing ~12.5% area changed",
      "image_path": null,
      "mask_path": null,
      "bounding_boxes": [
        {
          "label": "new_construction",
          "x_min": 50.0,
          "y_min": 120.0,
          "x_max": 150.0,
          "y_max": 240.0,
          "confidence": null
        }
      ],
      "metadata": {
        "change_ratio_percent": 12.5,
        "changed_regions_count": 2,
        "mock": true
      }
    }
  ],
  "visual_outputs": [],
  "metadata": {
    "adapter": "ChangeFormerMockAdapter"
  },
  "processing": {
    "duration_ms": 14,
    "steps": [
      { "step": "classify", "analysis_type": "CHANGE_DETECTION" },
      { "step": "adapter_selected", "model": "ChangeFormerV6 (mock)", "capability": "CHANGE_DETECTION" },
      { "step": "model_executed", "model": "ChangeFormerV6 (mock)", "mock": true },
      { "step": "complete", "duration_ms": 14 }
    ]
  },
  "errors": []
}
```

#### Structured Error Response
```json
{
  "request_id": "error",
  "analysis_type": null,
  "answer": "",
  "model_used": null,
  "confidence": null,
  "mock": false,
  "evidence": [],
  "visual_outputs": [],
  "metadata": {},
  "processing": { "duration_ms": 0, "steps": [] },
  "errors": [
    {
      "error_code": "UNSUPPORTED_FORMAT",
      "message": "Unsupported file format: .txt",
      "details": { "filename": "data.txt", "extension": "txt" }
    }
  ]
}
```
