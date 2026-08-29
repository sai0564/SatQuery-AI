"""
Unit tests for image validation and metadata extraction.
"""

import io
from PIL import Image
from backend.app.image_processing.validator import validate_file
from backend.app.image_processing.metadata import extract_metadata
from backend.app.utils.errors import (
    UnsupportedFormatError,
    FileTooLargeError,
    ImageDimensionError,
    ImageDecodeError,
)

def _create_test_image_bytes(size=(100, 100), fmt="PNG", mode="RGB") -> bytes:
    buf = io.BytesIO()
    img = Image.new(mode, size, color=(255, 0, 0))
    img.save(buf, format=fmt)
    return buf.getvalue()

def test_validate_valid_image():
    raw = _create_test_image_bytes(size=(256, 256), fmt="PNG")
    img = validate_file(raw, "test.png")
    assert isinstance(img, Image.Image)
    assert img.size == (256, 256)
    assert img.mode == "RGB"

def test_validate_unsupported_format():
    raw = b"some random text bytes"
    try:
        validate_file(raw, "test.txt")
        assert False, "Expected UnsupportedFormatError"
    except UnsupportedFormatError as exc:
        assert exc.error_code == "UNSUPPORTED_FORMAT"

def test_validate_corrupted_image():
    raw = b"not a valid png image data"
    try:
        validate_file(raw, "corrupt.png")
        assert False, "Expected ImageDecodeError"
    except ImageDecodeError as exc:
        assert exc.error_code == "IMAGE_DECODE_ERROR"

def test_validate_dimensions_too_small():
    raw = _create_test_image_bytes(size=(8, 8), fmt="PNG")
    try:
        validate_file(raw, "tiny.png")
        assert False, "Expected ImageDimensionError"
    except ImageDimensionError as exc:
        assert exc.error_code == "IMAGE_DIMENSION_ERROR"

def test_extract_metadata():
    img = Image.new("RGB", (300, 200), color=(0, 255, 0))
    meta = extract_metadata(img, filename="satellite.png")
    assert meta["width"] == 300
    assert meta["height"] == 200
    assert meta["mode"] == "RGB"
    assert meta["bands"] == 3
