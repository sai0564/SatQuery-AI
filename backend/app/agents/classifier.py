"""
SatQuery AI — Task Classifier.

Determines the analysis task type from image count, modality hints,
and query content. Uses a capability/task-based approach — NOT
hard-coded question strings.
"""

from typing import Any, Dict, List, Optional

from PIL import Image

from backend.app.models.base import ModelCapability
from backend.app.schemas.common import AnalysisType, ImageModality
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)


class TaskClassifier:
    """Classify user intent into an ``AnalysisType`` and required ``ModelCapability``."""

    @staticmethod
    def classify(
        images: List[Image.Image],
        query: str,
        modality_hint: Optional[ImageModality] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AnalysisType:
        """Determine analysis type from structural signals.

        Decision rules (in priority order):
        1. Two images + one is SAR → OPTICAL_SAR_ANALYSIS
        2. Two images → CHANGE_DETECTION
        3. One image → SINGLE_IMAGE_VQA
        """
        meta = metadata or {}
        num_images = len(images)

        if num_images == 0:
            return AnalysisType.UNKNOWN

        # ── Two-image scenarios ──────────────────────────────────
        if num_images >= 2:
            if modality_hint == ImageModality.SAR or meta.get("modality") == "sar":
                return AnalysisType.OPTICAL_SAR_ANALYSIS
            # Default two-image case: change detection
            return AnalysisType.CHANGE_DETECTION

        # ── Single-image scenarios ───────────────────────────────
        return AnalysisType.SINGLE_IMAGE_VQA

    @staticmethod
    def analysis_type_to_capability(analysis_type: AnalysisType) -> ModelCapability:
        """Map an analysis type to the primary model capability needed."""
        mapping = {
            AnalysisType.SINGLE_IMAGE_VQA: ModelCapability.SINGLE_IMAGE_VQA,
            AnalysisType.IMAGE_DESCRIPTION: ModelCapability.IMAGE_DESCRIPTION,
            AnalysisType.CHANGE_DETECTION: ModelCapability.CHANGE_DETECTION,
            AnalysisType.BI_TEMPORAL_ANALYSIS: ModelCapability.BI_TEMPORAL_ANALYSIS,
            AnalysisType.OPTICAL_SAR_ANALYSIS: ModelCapability.OPTICAL_SAR_ANALYSIS,
        }
        return mapping.get(analysis_type, ModelCapability.SINGLE_IMAGE_VQA)
