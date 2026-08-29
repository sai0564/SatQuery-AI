"""
Optical imagery preprocessing pipeline.
Handles RGB/multispectral normalization, contrast stretching, and tiling.
"""

from typing import Any, Dict, Optional
from PIL import Image

class OpticalPreprocessor:
    @staticmethod
    def normalize_optical(image: Image.Image) -> Image.Image:
        """Applies standard normalization and RGB conversion."""
        if image.mode != "RGB":
            return image.convert("RGB")
        return image
