"""
ChangeFormer Adapter Interface.

Real implementation on ``feature/changeformer-agent``.
"""

from typing import List, Optional

from backend.app.models.base import (
    AnalysisInput,
    AnalysisResult,
    BaseModelAdapter,
    ModelCapability,
)


class ChangeFormerAdapter(BaseModelAdapter):
    """Real ChangeFormerV6 adapter (to be implemented on feature/changeformer-agent)."""

    def get_model_name(self) -> str:
        return "ChangeFormerV6"

    def get_capabilities(self) -> List[ModelCapability]:
        return [ModelCapability.CHANGE_DETECTION, ModelCapability.BI_TEMPORAL_ANALYSIS]

    def validate_input(self, analysis_input: AnalysisInput) -> Optional[str]:
        if len(analysis_input.images) < 2:
            return "Change detection requires exactly two images (T1 and T2)."
        return None

    def analyze(self, analysis_input: AnalysisInput) -> AnalysisResult:
        raise NotImplementedError(
            "Real ChangeFormerV6 inference is not yet integrated. "
            "Set USE_MOCK_MODELS=true or implement on feature/changeformer-agent."
        )
