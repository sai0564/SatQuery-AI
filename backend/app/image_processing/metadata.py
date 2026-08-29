"""
SatQuery AI — Image Metadata Extraction.

Extracts basic metadata from PIL images (dimensions, mode, bands).
Extended later for EXIF, geotiff tags, etc.
"""

from typing import Any, Dict

from PIL import Image


def extract_metadata(image: Image.Image, filename: str = "") -> Dict[str, Any]:
    """Return basic metadata for a validated PIL image."""
    w, h = image.size
    return {
        "filename": filename,
        "width": w,
        "height": h,
        "mode": image.mode,
        "bands": len(image.getbands()),
        "format": getattr(image, "format", None),
    }
