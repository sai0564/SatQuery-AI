"""
API Route Handlers for SatQuery AI.
Exposes endpoints for health checks and multimodal agent analysis.
"""

from fastapi import APIRouter, HTTPException, Depends
from backend.api.schemas import AnalysisRequest, AnalysisResponse, HealthResponse
from backend.services.agent_service import AgentService

router = APIRouter(prefix="/api/v1", tags=["Analysis"])

# Dependency injection for AgentService
def get_agent_service() -> AgentService:
    return AgentService()

@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Returns system status and list of registered models."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        models_available=["GeoChat-7B", "ChangeFormerV6", "BIFOLD-RDNet"]
    )

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_images(
    request: AnalysisRequest,
    service: AgentService = Depends(get_agent_service)
):
    """
    Primary agentic vision-language analysis endpoint.
    Accepts single image, bi-temporal pair, or Optical+SAR image input with query.
    """
    try:
        payload = request.model_dump()
        result = service.process_analysis_request(payload)
        return AnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
