"""
SatQuery AI — Analysis API Routes.

POST /api/v1/analyze  — accepts multipart file uploads + JSON query
GET  /api/v1/health   — system status
"""

import json
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile

from backend.app.api.dependencies import get_analysis_service, get_registry
from backend.app.config.settings import settings
from backend.app.schemas.common import ErrorDetail, ImageModality, ProcessingInfo
from backend.app.schemas.responses import AnalysisResponse, HealthResponse
from backend.app.services.analysis_service import AnalysisService
from backend.app.utils.errors import SatQueryError
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Analysis"])


# ── Health ───────────────────────────────────────────────────────


@router.get("/health", response_model=HealthResponse)
def health_check():
    """System health and registered capabilities."""
    registry = get_registry()
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        mock_mode=settings.USE_MOCK_MODELS,
        models_registered=registry.list_models(),
        capabilities=registry.list_capabilities(),
    )


# ── Analyze ──────────────────────────────────────────────────────


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    files: List[UploadFile] = File(..., description="One or more satellite images"),
    query: str = Form(default="Describe this image."),
    modality: Optional[str] = Form(default=None),
    metadata: Optional[str] = Form(default=None, description="JSON string of metadata"),
    service: AnalysisService = Depends(get_analysis_service),
):
    """Analyze uploaded satellite imagery with a natural-language query.

    Accepts:
    - **files**: one or more image files (JPEG, PNG, TIFF)
    - **query**: natural-language question or instruction
    - **modality**: optional hint — ``optical`` or ``sar``
    - **metadata**: optional JSON string with extra info (dates, sensor, etc.)
    """
    try:
        # Read uploaded file bytes
        file_pairs = []
        for f in files:
            raw = await f.read()
            file_pairs.append((f.filename or "upload.png", raw))

        modality_hint = None
        if modality:
            try:
                modality_hint = ImageModality(modality)
            except ValueError:
                pass

        meta = {}
        if metadata:
            try:
                meta = json.loads(metadata)
            except json.JSONDecodeError:
                pass

        result = await service.analyze(
            files=file_pairs,
            query=query,
            modality_hint=modality_hint,
            metadata=meta,
        )

        return AnalysisResponse(
            request_id=result["request_id"],
            analysis_type=result.get("analysis_type"),
            answer=result.get("answer", ""),
            model_used=result.get("model_used"),
            confidence=result.get("confidence"),
            mock=result.get("mock", False),
            evidence=result.get("evidence", []),
            visual_outputs=result.get("visual_outputs", []),
            metadata=result.get("metadata", {}),
            processing=ProcessingInfo(**result.get("processing", {})),
            errors=[],
        )

    except SatQueryError as exc:
        logger.warning("Analysis error: %s", exc.message)
        return AnalysisResponse(
            request_id="error",
            answer="",
            errors=[
                ErrorDetail(
                    error_code=exc.error_code,
                    message=exc.message,
                    details=exc.details,
                )
            ],
        )
    except Exception as exc:
        logger.exception("Unexpected error during analysis")
        return AnalysisResponse(
            request_id="error",
            answer="",
            errors=[
                ErrorDetail(
                    error_code="INTERNAL_ERROR",
                    message="An unexpected error occurred.",
                    details={},
                )
            ],
        )
