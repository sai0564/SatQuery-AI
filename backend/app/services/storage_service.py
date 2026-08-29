"""
SatQuery AI — Storage Abstraction.

Local filesystem backend for development. The interface is designed so
that S3 / Azure Blob / GCP can be plugged in later.
"""

import shutil
import uuid
from pathlib import Path
from typing import Optional

from backend.app.config.settings import settings
from backend.app.utils.errors import StorageError
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)


class StorageService:
    """Abstract-ish storage that currently uses the local filesystem."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or settings.UPLOAD_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_bytes(self, data: bytes, filename: str, subdir: str = "") -> str:
        """Save raw bytes and return the relative path."""
        unique = f"{uuid.uuid4().hex[:8]}_{filename}"
        dest = self.base_dir / subdir / unique if subdir else self.base_dir / unique
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            dest.write_bytes(data)
        except OSError as exc:
            raise StorageError("save_bytes", str(exc))
        logger.info("Saved %s (%d bytes)", dest, len(data))
        return str(dest)

    def save_image(self, image, filename: str, subdir: str = "") -> str:
        """Save a PIL Image as PNG and return the relative path."""
        unique = f"{uuid.uuid4().hex[:8]}_{Path(filename).stem}.png"
        dest = self.base_dir / subdir / unique if subdir else self.base_dir / unique
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            image.save(str(dest), format="PNG")
        except OSError as exc:
            raise StorageError("save_image", str(exc))
        logger.info("Saved image %s", dest)
        return str(dest)

    def delete(self, path: str) -> None:
        """Delete a stored file."""
        try:
            Path(path).unlink(missing_ok=True)
        except OSError as exc:
            raise StorageError("delete", str(exc))
