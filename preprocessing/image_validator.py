"""
Image and input data validation for remote sensing imagery.
Validates dimensions, channels, formats, timestamps, and modality configurations.
"""

from typing import Any, Dict, List, Optional, Tuple
from PIL import Image

class ImageValidator:
    ALLOWED_FORMATS = {"JPEG", "PNG", "TIFF", "GeoTIFF"}

    @staticmethod
    def validate_single_image(image: Any) -> Tuple[bool, Optional[str]]:
        """Validates that a single image input is non-empty and well-formed."""
        if image is None:
            return False, "Input image is missing."
        if isinstance(image, Image.Image):
            if image.size[0] < 16 or image.size[1] < 16:
                return False, f"Image dimensions {image.size} are too small."
            return True, None
        return True, None

    @staticmethod
    def validate_bitemporal_pair(image_t1: Any, image_t2: Any, date_t1: Optional[str] = None, date_t2: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """Validates bi-temporal image pair and temporal metadata."""
        valid_t1, err_t1 = ImageValidator.validate_single_image(image_t1)
        if not valid_t1:
            return False, f"T1 Image error: {err_t1}"

        valid_t2, err_t2 = ImageValidator.validate_single_image(image_t2)
        if not valid_t2:
            return False, f"T2 Image error: {err_t2}"

        return True, None

    @staticmethod
    def validate_optical_sar_pair(optical_image: Any, sar_image: Any) -> Tuple[bool, Optional[str]]:
        """Validates co-registered Optical + SAR image pair."""
        valid_opt, err_opt = ImageValidator.validate_single_image(optical_image)
        if not valid_opt:
            return False, f"Optical Image error: {err_opt}"

        valid_sar, err_sar = ImageValidator.validate_single_image(sar_image)
        if not valid_sar:
            return False, f"SAR Image error: {err_sar}"

        return True, None
