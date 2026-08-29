"""
SatQuery AI — Base Model Adapter.

Every specialist model (GeoChat, ChangeFormer, BIFOLD) plugs into the
system through this adapter interface. The router never sees model
internals — only capabilities and the ``analyze()`` contract.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ── Capabilities ─────────────────────────────────────────────────


class ModelCapability(str, Enum):
    """Capabilities a model adapter can declare."""

    SINGLE_IMAGE_VQA = "SINGLE_IMAGE_VQA"
    IMAGE_DESCRIPTION = "IMAGE_DESCRIPTION"
    CHANGE_DETECTION = "CHANGE_DETECTION"
    BI_TEMPORAL_ANALYSIS = "BI_TEMPORAL_ANALYSIS"
    OPTICAL_SAR_ANALYSIS = "OPTICAL_SAR_ANALYSIS"


# ── Structured I/O ───────────────────────────────────────────────


class AnalysisInput(BaseModel):
    """Structured input handed to an adapter."""

    images: List[Any] = Field(
        default_factory=list,
        description="List of PIL.Image objects (order matters: [t1, t2] or [optical, sar])",
    )
    query: str = "Describe this image."
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AnalysisResult(BaseModel):
    """Structured output returned by an adapter."""

    model_name: str
    analysis_type: str
    answer: str = ""
    confidence: Optional[float] = Field(
        default=None,
        description="null unless the real model produces a calibrated score",
    )
    mock: bool = False
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    visual_outputs: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ── Abstract Adapter ─────────────────────────────────────────────


class BaseModelAdapter(ABC):
    """Interface that every model adapter must implement.

    The router interacts only with this interface. Model-specific
    logic is hidden inside each concrete adapter.
    """

    @abstractmethod
    def get_model_name(self) -> str:
        """Return a human-readable model identifier."""

    @abstractmethod
    def get_capabilities(self) -> List[ModelCapability]:
        """Declare which capabilities this adapter supports."""

    @abstractmethod
    def validate_input(self, analysis_input: AnalysisInput) -> Optional[str]:
        """Validate whether the input is sufficient.

        Returns ``None`` if valid, or an error message string.
        """

    @abstractmethod
    def analyze(self, analysis_input: AnalysisInput) -> AnalysisResult:
        """Run inference and return a structured result."""
