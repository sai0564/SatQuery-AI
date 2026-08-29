"""
SatQuery AI — Common Schema Types.

Shared enums, evidence types, and base structures used across requests
and responses.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ── Analysis Task Types ──────────────────────────────────────────


class AnalysisType(str, Enum):
    """Capability-based task types the system can perform."""

    SINGLE_IMAGE_VQA = "SINGLE_IMAGE_VQA"
    IMAGE_DESCRIPTION = "IMAGE_DESCRIPTION"
    CHANGE_DETECTION = "CHANGE_DETECTION"
    BI_TEMPORAL_ANALYSIS = "BI_TEMPORAL_ANALYSIS"
    OPTICAL_SAR_ANALYSIS = "OPTICAL_SAR_ANALYSIS"
    UNKNOWN = "UNKNOWN"


class ImageModality(str, Enum):
    """Sensor modality of an uploaded image."""

    OPTICAL = "optical"
    SAR = "sar"
    UNKNOWN = "unknown"


# ── Evidence Structures ──────────────────────────────────────────


class BoundingBox(BaseModel):
    label: str = ""
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    confidence: Optional[float] = None


class EvidenceItem(BaseModel):
    """A single piece of visual or analytical evidence."""

    type: str = Field(
        ..., description="E.g. 'highlighted_image', 'change_map', 'bounding_boxes', 'overlay'"
    )
    description: str = ""
    image_path: Optional[str] = None
    mask_path: Optional[str] = None
    bounding_boxes: List[BoundingBox] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ── Processing Metadata ─────────────────────────────────────────


class ProcessingInfo(BaseModel):
    duration_ms: int = 0
    steps: List[Dict[str, Any]] = Field(default_factory=list)


# ── Error Detail ─────────────────────────────────────────────────


class ErrorDetail(BaseModel):
    error_code: str
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)
