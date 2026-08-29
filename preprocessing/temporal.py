"""
Temporal alignment and co-registration preprocessor.
Ensures bi-temporal or multi-sensor image pairs share spatial bounds and pixel resolution.
"""

from typing import Any, Dict, Tuple
from PIL import Image

class TemporalPreprocessor:
    @staticmethod
    def align_pair(image_t1: Image.Image, image_t2: Image.Image) -> Tuple[Image.Image, Image.Image]:
        """Ensures both images in a bi-temporal pair match in resolution and dimensions."""
        if image_t1.size != image_t2.size:
            image_t2 = image_t2.resize(image_t1.size, Image.Resampling.BILINEAR)
        return image_t1, image_t2
