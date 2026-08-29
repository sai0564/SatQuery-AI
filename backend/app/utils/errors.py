"""
SatQuery AI — Structured Error Handling.

All user-facing errors are structured and safe.
Internal details are logged but never exposed to clients.
"""

from typing import Any, Dict, List, Optional


class SatQueryError(Exception):
    """Base exception for all SatQuery AI errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
        }


# ── Validation Errors ────────────────────────────────────────────


class ImageValidationError(SatQueryError):
    """Raised when an uploaded image fails validation."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="IMAGE_VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class UnsupportedFormatError(SatQueryError):
    """Raised when an image format is not supported."""

    def __init__(self, filename: str, extension: str):
        super().__init__(
            message=f"Unsupported file format: .{extension}",
            error_code="UNSUPPORTED_FORMAT",
            status_code=422,
            details={"filename": filename, "extension": extension},
        )


class FileTooLargeError(SatQueryError):
    """Raised when an uploaded file exceeds the size limit."""

    def __init__(self, filename: str, size_mb: float, limit_mb: int):
        super().__init__(
            message=f"File too large: {size_mb:.1f} MB (limit: {limit_mb} MB)",
            error_code="FILE_TOO_LARGE",
            status_code=413,
            details={"filename": filename, "size_mb": size_mb, "limit_mb": limit_mb},
        )


class ImageDecodeError(SatQueryError):
    """Raised when an image file cannot be decoded."""

    def __init__(self, filename: str):
        super().__init__(
            message=f"Cannot decode image file: {filename}",
            error_code="IMAGE_DECODE_ERROR",
            status_code=422,
            details={"filename": filename},
        )


class ImageDimensionError(SatQueryError):
    """Raised when image dimensions are outside allowed bounds."""

    def __init__(self, width: int, height: int, min_dim: int, max_dim: int):
        super().__init__(
            message=f"Image dimensions {width}x{height} outside allowed range [{min_dim}, {max_dim}]",
            error_code="IMAGE_DIMENSION_ERROR",
            status_code=422,
            details={
                "width": width,
                "height": height,
                "min_dimension": min_dim,
                "max_dimension": max_dim,
            },
        )


# ── Analysis Errors ──────────────────────────────────────────────


class MissingImageError(SatQueryError):
    """Raised when required images are not provided."""

    def __init__(self, message: str = "At least one image is required."):
        super().__init__(
            message=message,
            error_code="MISSING_IMAGE",
            status_code=422,
        )


class IncompatibleImagePairError(SatQueryError):
    """Raised when a bi-temporal pair has incompatible images."""

    def __init__(self, reason: str):
        super().__init__(
            message=f"Incompatible image pair: {reason}",
            error_code="INCOMPATIBLE_IMAGE_PAIR",
            status_code=422,
            details={"reason": reason},
        )


class UnsupportedTaskError(SatQueryError):
    """Raised when the router cannot determine a valid analysis task."""

    def __init__(self, message: str = "Unable to determine analysis task from inputs."):
        super().__init__(
            message=message,
            error_code="UNSUPPORTED_TASK",
            status_code=422,
        )


class ModelUnavailableError(SatQueryError):
    """Raised when no adapter is registered for a required capability."""

    def __init__(self, capability: str):
        super().__init__(
            message=f"No model available for capability: {capability}",
            error_code="MODEL_UNAVAILABLE",
            status_code=503,
            details={"capability": capability},
        )


class ModelExecutionError(SatQueryError):
    """Raised when a model adapter fails during execution."""

    def __init__(self, model_name: str, reason: str):
        super().__init__(
            message=f"Model execution failed: {model_name}",
            error_code="MODEL_EXECUTION_ERROR",
            status_code=500,
            details={"model": model_name, "reason": reason},
        )


class StorageError(SatQueryError):
    """Raised when a storage operation fails."""

    def __init__(self, operation: str, reason: str):
        super().__init__(
            message=f"Storage error during {operation}",
            error_code="STORAGE_ERROR",
            status_code=500,
            details={"operation": operation, "reason": reason},
        )
