"""
ChangeFormer Mock Adapter.

Returns clearly-labelled mock change-detection results.
Every response contains ``mock: true`` and ``confidence: null``.
"""

from typing import List, Optional

from backend.app.models.base import (
    AnalysisInput,
    AnalysisResult,
    BaseModelAdapter,
    ModelCapability,
)


class ChangeFormerMockAdapter(BaseModelAdapter):
    """Mock adapter standing in for the real ChangeFormerV6 model."""

    def get_model_name(self) -> str:
        return "ChangeFormerV6 (mock)"

    def get_capabilities(self) -> List[ModelCapability]:
        return [ModelCapability.CHANGE_DETECTION, ModelCapability.BI_TEMPORAL_ANALYSIS]

    def validate_input(self, analysis_input: AnalysisInput) -> Optional[str]:
        if len(analysis_input.images) < 2:
            return "Change detection requires exactly two images (T1 and T2)."
        return None

    def analyze(self, analysis_input: AnalysisInput) -> AnalysisResult:
        query = analysis_input.query

        mock_answer = (
            f"[MOCK] This is a simulated ChangeFormerV6 response. "
            f"Query: '{query}'. In a real deployment, ChangeFormerV6 would "
            f"compare the two bi-temporal images and produce a change map "
            f"highlighting areas of construction, vegetation loss, water-body "
            f"changes, and other land-cover transitions."
        )

        mock_evidence = [
            {
                "type": "change_map",
                "description": "[MOCK] Simulated change map showing ~12.5% area changed",
                "bounding_boxes": [
                    {"label": "new_construction", "x_min": 50, "y_min": 120, "x_max": 150, "y_max": 240},
                    {"label": "vegetation_loss", "x_min": 200, "y_min": 300, "x_max": 280, "y_max": 410},
                ],
                "metadata": {
                    "change_ratio_percent": 12.5,
                    "changed_regions_count": 2,
                    "mock": True,
                },
            }
        ]

        return AnalysisResult(
            model_name=self.get_model_name(),
            analysis_type=ModelCapability.CHANGE_DETECTION.value,
            answer=mock_answer,
            confidence=None,
            mock=True,
            evidence=mock_evidence,
            visual_outputs=[],
            metadata={"adapter": "ChangeFormerMockAdapter"},
        )
