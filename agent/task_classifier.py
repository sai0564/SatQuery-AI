"""
Task Classifier for multimodal remote-sensing requests.
Categorizes user inputs based on image modalities, timestamps, and query intent.
"""

from enum import Enum
from typing import Any, Dict, Optional

class TaskType(str, Enum):
    SINGLE_IMAGE_VQA_CAPTION = "single_image_vqa_caption"
    CHANGE_DETECTION_EXPLANATION = "change_detection_explanation"
    OPTICAL_SAR_FUSION = "optical_sar_fusion"
    UNKNOWN = "unknown"

class TaskClassifier:
    @staticmethod
    def classify(input_data: Dict[str, Any], query: Optional[str] = None) -> TaskType:
        """
        Determines the target workflow based on input structure and query.

        Rules:
        - Optical + SAR present -> OPTICAL_SAR_FUSION
        - Two images / bi-temporal dates present -> CHANGE_DETECTION_EXPLANATION
        - Single image present -> SINGLE_IMAGE_VQA_CAPTION
        """
        has_optical = "optical_image" in input_data and input_data["optical_image"] is not None
        has_sar = "sar_image" in input_data and input_data["sar_image"] is not None

        if has_optical and has_sar:
            return TaskType.OPTICAL_SAR_FUSION

        has_t1 = "image_t1" in input_data and input_data["image_t1"] is not None
        has_t2 = "image_t2" in input_data and input_data["image_t2"] is not None

        if has_t1 and has_t2:
            return TaskType.CHANGE_DETECTION_EXPLANATION

        has_single = ("image" in input_data and input_data["image"] is not None) or (has_t1 and not has_t2)
        if has_single:
            return TaskType.SINGLE_IMAGE_VQA_CAPTION

        return TaskType.UNKNOWN
