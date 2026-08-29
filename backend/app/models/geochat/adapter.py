"""
GeoChat Adapter Interface.

The real implementation will be developed on the ``feature/geochat-agent``
branch. This file defines only the adapter class to be completed later.
"""

from typing import List, Optional

from backend.app.models.base import (
    AnalysisInput,
    AnalysisResult,
    BaseModelAdapter,
    ModelCapability,
)


class GeoChatAdapter(BaseModelAdapter):
    """Real GeoChat-7B adapter (to be implemented on feature/geochat-agent)."""

    def get_model_name(self) -> str:
        return "GeoChat-7B"

    def get_capabilities(self) -> List[ModelCapability]:
        return [ModelCapability.SINGLE_IMAGE_VQA, ModelCapability.IMAGE_DESCRIPTION]

    def validate_input(self, analysis_input: AnalysisInput) -> Optional[str]:
        if not analysis_input.images:
            return "GeoChat requires at least one image."
        return None

    def analyze(self, analysis_input: AnalysisInput) -> AnalysisResult:
        raise NotImplementedError(
            "Real GeoChat-7B inference is not yet integrated. "
            "Set USE_MOCK_MODELS=true or implement on feature/geochat-agent."
        )
