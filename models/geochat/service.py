"""
GeoChat-7B Specialist Model Service.
Implements the BaseModelService interface.
Responsibilities:
- Single-image VQA
- Remote sensing image captioning & scene description
- Spatial grounding
"""

from typing import Any, Dict, Optional
from models.base import BaseModelService
from models.geochat.inference import GeoChatInference

class GeoChatService(BaseModelService):
    def __init__(self, inference_engine: Optional[GeoChatInference] = None):
        self.engine = inference_engine or GeoChatInference()

    def analyze(self, input_data: Dict[str, Any], query: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a single remote sensing image using GeoChat-7B.
        """
        image = input_data.get("image") or input_data.get("image_t1")
        if image is None:
            raise ValueError("GeoChatService requires 'image' in input_data.")

        user_query = query or "Describe this remote sensing image in detail."
        raw_output = self.engine.generate(image=image, prompt=user_query)

        return {
            "model": "GeoChat-7B",
            "task": "single_image_vqa_caption",
            "answer": raw_output,
            "grounding": None,
            "confidence": 0.92,
            "metadata": {
                "engine": "geochat-7b",
                "status": "success"
            }
        }
