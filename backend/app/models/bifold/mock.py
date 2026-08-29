"""
BIFOLD Mock Adapter.

Returns clearly-labelled mock Optical + SAR fusion results.
Every response contains ``mock: true`` and ``confidence: null``.
"""

from typing import List, Optional

from backend.app.models.base import (
    AnalysisInput,
    AnalysisResult,
    BaseModelAdapter,
    ModelCapability,
)


class BifoldMockAdapter(BaseModelAdapter):
    """Mock adapter standing in for the real BIFOLD RDNet model."""

    def get_model_name(self) -> str:
        return "BIFOLD-RDNet (mock)"

    def get_capabilities(self) -> List[ModelCapability]:
        return [ModelCapability.OPTICAL_SAR_ANALYSIS]

    def validate_input(self, analysis_input: AnalysisInput) -> Optional[str]:
        if len(analysis_input.images) < 2:
            return "Optical+SAR analysis requires exactly two images (optical and SAR)."
        return None

    def analyze(self, analysis_input: AnalysisInput) -> AnalysisResult:
        query = analysis_input.query

        mock_answer = (
            f"[MOCK] This is a simulated BIFOLD RDNet response. "
            f"Query: '{query}'. In a real deployment, BIFOLD would fuse "
            f"co-registered optical and SAR imagery through a dual-branch "
            f"encoder, detecting structures invisible to optical sensors "
            f"alone (e.g. through cloud cover, canopy, or darkness)."
        )

        mock_evidence = [
            {
                "type": "fusion_result",
                "description": "[MOCK] Simulated Optical+SAR feature fusion",
                "metadata": {
                    "sar_penetration_indicators": {
                        "subsurface_structure_detected": True,
                        "cloud_occlusion_mitigated": True,
                    },
                    "detected_targets": [
                        {"class": "vessel_metallic_signature", "bbox": [110, 80, 175, 140]},
                        {"class": "runway_infrastructure", "bbox": [320, 210, 480, 270]},
                    ],
                    "mock": True,
                },
            }
        ]

        return AnalysisResult(
            model_name=self.get_model_name(),
            analysis_type=ModelCapability.OPTICAL_SAR_ANALYSIS.value,
            answer=mock_answer,
            confidence=None,
            mock=True,
            evidence=mock_evidence,
            visual_outputs=[],
            metadata={"adapter": "BifoldMockAdapter"},
        )
