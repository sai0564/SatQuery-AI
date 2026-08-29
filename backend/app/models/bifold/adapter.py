"""
BIFOLD Adapter Interface.

Real implementation on ``feature/optical-sar-agent``.
"""

from typing import List, Optional

from backend.app.models.base import (
    AnalysisInput,
    AnalysisResult,
    BaseModelAdapter,
    ModelCapability,
)


class BifoldAdapter(BaseModelAdapter):
    """Real BIFOLD RDNet adapter (to be implemented on feature/optical-sar-agent)."""

    def get_model_name(self) -> str:
        return "BIFOLD-RDNet"

    def get_capabilities(self) -> List[ModelCapability]:
        return [ModelCapability.OPTICAL_SAR_ANALYSIS]

    def validate_input(self, analysis_input: AnalysisInput) -> Optional[str]:
        if len(analysis_input.images) < 2:
            return "Optical+SAR analysis requires exactly two images (optical and SAR)."
        return None

    def analyze(self, analysis_input: AnalysisInput) -> AnalysisResult:
        raise NotImplementedError(
            "Real BIFOLD RDNet inference is not yet integrated. "
            "Set USE_MOCK_MODELS=true or implement on feature/optical-sar-agent."
        )
