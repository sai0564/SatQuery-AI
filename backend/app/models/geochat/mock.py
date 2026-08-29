"""
GeoChat Mock Adapter.

Placeholder that returns clearly-labelled mock results so the full
application can run end-to-end without a GPU.

Every response contains ``mock: true`` and ``confidence: null``.
"""

from typing import List, Optional

from backend.app.models.base import (
    AnalysisInput,
    AnalysisResult,
    BaseModelAdapter,
    ModelCapability,
)


class GeoChatMockAdapter(BaseModelAdapter):
    """Mock adapter standing in for the real GeoChat-7B model."""

    def get_model_name(self) -> str:
        return "GeoChat-7B (mock)"

    def get_capabilities(self) -> List[ModelCapability]:
        return [ModelCapability.SINGLE_IMAGE_VQA, ModelCapability.IMAGE_DESCRIPTION]

    def validate_input(self, analysis_input: AnalysisInput) -> Optional[str]:
        if not analysis_input.images:
            return "GeoChat requires at least one image."
        return None

    def analyze(self, analysis_input: AnalysisInput) -> AnalysisResult:
        query = analysis_input.query

        mock_answer = (
            f"[MOCK] This is a simulated GeoChat-7B response to the query: "
            f"'{query}'. In a real deployment, GeoChat-7B would analyze the "
            f"satellite image and provide a detailed scene description, "
            f"identify land-use patterns, buildings, vegetation, water bodies, "
            f"and other features visible in the remote sensing imagery."
        )

        return AnalysisResult(
            model_name=self.get_model_name(),
            analysis_type=ModelCapability.SINGLE_IMAGE_VQA.value,
            answer=mock_answer,
            confidence=None,
            mock=True,
            evidence=[],
            visual_outputs=[],
            metadata={"adapter": "GeoChatMockAdapter"},
        )
