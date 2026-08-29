from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseModelService(ABC):
    """
    Abstract base class defining the common interface for all specialist models.
    Each model (GeoChat, ChangeFormer, BIFOLD) must implement this interface independently.
    """

    @abstractmethod
    def analyze(self, input_data: Dict[str, Any], query: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute model inference on input data.

        Args:
            input_data: Dictionary containing images, metadata, and optional temporal/modality info.
                Example keys:
                - "image": PIL.Image or path (for single image)
                - "image_t1", "image_t2": Bi-temporal image pair
                - "optical_image", "sar_image": Optical + SAR image pair
            query: Optional natural language instruction or question.

        Returns:
            Dict containing model specific outputs (e.g. text answer, change mask, bounding boxes, confidence).
        """
        pass
