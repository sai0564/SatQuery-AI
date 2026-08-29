"""
SatQuery AI — Image Validation.

Validates uploaded image files: format, size, decodability, dimensions.
Model-specific preprocessing is NOT done here — it belongs inside the
model adapter.
"""

import io
from typing import Optional, Tuple

from PIL import Image

from backend.app.config.settings import settings
from backend.app.utils.errors import (
    FileTooLargeError,
    ImageDecodeError,
    ImageDimensionError,
    ImageValidationError,
    UnsupportedFormatError,
)
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)


def _extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def validate_file(file_bytes: bytes, filename: str) -> Image.Image:
    """Validate an uploaded image file and return a PIL Image.

    Raises a subclass of ``SatQueryError`` on failure.
    """
    ext = _extension(filename)
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise UnsupportedFormatError(filename, ext)

    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise FileTooLargeError(filename, size_mb, settings.MAX_UPLOAD_SIZE_MB)

    try:
        image = Image.open(io.BytesIO(file_bytes))
        image.load()  # force full decode
    except Exception:
        raise ImageDecodeError(filename)

    w, h = image.size
    if w < settings.MIN_IMAGE_DIMENSION or h < settings.MIN_IMAGE_DIMENSION:
        raise ImageDimensionError(w, h, settings.MIN_IMAGE_DIMENSION, settings.MAX_IMAGE_DIMENSION)
    if w > settings.MAX_IMAGE_DIMENSION or h > settings.MAX_IMAGE_DIMENSION:
        raise ImageDimensionError(w, h, settings.MIN_IMAGE_DIMENSION, settings.MAX_IMAGE_DIMENSION)

    logger.info("Validated image %s (%dx%d, %.1f MB)", filename, w, h, size_mb)
    return image.convert("RGB")
