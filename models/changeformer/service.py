"""
ChangeFormerV6 Specialist Model Service.
Implements the BaseModelService interface.
Responsibilities:
- Bi-temporal change detection
- Produce change map & changed region coordinates
"""

from typing import Any, Dict, Optional
from models.base import BaseModelService
from models.changeformer.inference import ChangeFormerInference

class ChangeFormerService(BaseModelService):
    def __init__(self, inference_engine: Optional[ChangeFormerInference] = None):
        self.engine = inference_engine or ChangeFormerInference()

    def analyze(self, input_data: Dict[str, Any], query: Optional[str] = None) -> Dict[str, Any]:
        """
        Detect changes across a bi-temporal image pair (T1, T2).
        """
        image_t1 = input_data.get("image_t1")
        image_t2 = input_data.get("image_t2")

        if image_t1 is None or image_t2 is None:
            raise ValueError("ChangeFormerService requires both 'image_t1' and 'image_t2' in input_data.")

        change_results = self.engine.predict_change(image_t1=image_t1, image_t2=image_t2)

        return {
            "model": "ChangeFormerV6",
            "task": "bitemporal_change_detection",
            "answer": f"Detected significant spatial changes covering ~{change_results['change_ratio_percentage']}% of the area.",
            "evidence": {
                "change_map_available": True,
                "change_ratio": change_results["change_ratio_percentage"],
                "changed_regions": change_results["bounding_boxes"],
                "total_changed_regions": change_results["changed_regions_count"]
            },
            "confidence": 0.89,
            "metadata": {
                "engine": "changeformer-v6",
                "status": "success"
            }
        }
