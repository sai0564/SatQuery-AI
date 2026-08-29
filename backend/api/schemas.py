"""
Pydantic API Schemas for SatQuery AI.
Defines input payloads, response models, and trace structures.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    query: Optional[str] = Field(default="Describe this image.", description="User natural language question or prompt")
    image: Optional[str] = Field(default=None, description="Base64 encoded string or URL for single image")
    image_t1: Optional[str] = Field(default=None, description="Base64 encoded string or URL for T1 (bi-temporal)")
    image_t2: Optional[str] = Field(default=None, description="Base64 encoded string or URL for T2 (bi-temporal)")
    date_t1: Optional[str] = Field(default=None, description="Timestamp/date for T1 image")
    date_t2: Optional[str] = Field(default=None, description="Timestamp/date for T2 image")
    optical_image: Optional[str] = Field(default=None, description="Optical image data or URL")
    sar_image: Optional[str] = Field(default=None, description="SAR image data or URL")

class ExecutionTraceStep(BaseModel):
    step: str
    model: Optional[str] = None
    action: Optional[str] = None
    task_type: Optional[str] = None
    timestamp: Optional[float] = None
    message: Optional[str] = None

class AnalysisResponse(BaseModel):
    answer: str
    evidence: Dict[str, Any] = Field(default_factory=dict)
    confidence: float
    execution_trace: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class HealthResponse(BaseModel):
    status: str
    version: str
    models_available: List[str]
