"""
SatQuery AI — Response Schemas.

Structured response matching §12 of the architecture specification.
Supports both real and mock model implementations.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from backend.app.schemas.common import (
    AnalysisType,
    ErrorDetail,
    EvidenceItem,
    ProcessingInfo,
)


class AnalysisResponse(BaseModel):
    """The primary response contract returned by POST /api/v1/analyze."""

    request_id: str = Field(..., description="Unique identifier for this request")
    analysis_type: Optional[str] = Field(
        default=None, description="The determined analysis task type"
    )
    answer: str = Field(default="", description="Natural-language answer")
    model_used: Optional[str] = Field(
        default=None, description="Name of the model adapter that produced the answer"
    )
    confidence: Optional[float] = Field(
        default=None,
        description="Model confidence score (null if the model does not provide one)",
    )
    mock: bool = Field(
        default=False,
        description="True when the result was produced by a mock adapter",
    )
    evidence: List[EvidenceItem] = Field(default_factory=list)
    visual_outputs: List[str] = Field(
        default_factory=list,
        description="Paths or URLs to generated visual outputs",
    )
    metadata: Dict[str, Any] = Field(default_factory=dict)
    processing: ProcessingInfo = Field(default_factory=ProcessingInfo)
    errors: List[ErrorDetail] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """GET /api/v1/health response."""

    status: str
    version: str
    mock_mode: bool
    models_registered: List[str]
    capabilities: List[str]
