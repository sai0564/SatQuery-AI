"""
SatQuery AI — Application Configuration.

All settings are loaded from environment variables with sensible defaults
for local development. Never hard-code secrets.
"""

import os
from pathlib import Path
from typing import List


class Settings:
    """Central configuration loaded from environment variables."""

    # ── Application ──────────────────────────────────────────────
    APP_NAME: str = "SatQuery AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # ── API ──────────────────────────────────────────────────────
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
    ).split(",")

    # ── Upload limits ────────────────────────────────────────────
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
    MAX_IMAGE_DIMENSION: int = int(os.getenv("MAX_IMAGE_DIMENSION", "10000"))
    MIN_IMAGE_DIMENSION: int = int(os.getenv("MIN_IMAGE_DIMENSION", "16"))
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "tif", "tiff"]

    # ── Storage ──────────────────────────────────────────────────
    STORAGE_BACKEND: str = os.getenv("STORAGE_BACKEND", "local")  # local | s3
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", "uploads"))
    EVIDENCE_DIR: Path = Path(os.getenv("EVIDENCE_DIR", "evidence_outputs"))

    # ── Model configuration ──────────────────────────────────────
    USE_MOCK_MODELS: bool = os.getenv("USE_MOCK_MODELS", "true").lower() == "true"
    MODEL_DEVICE: str = os.getenv("MODEL_DEVICE", "cpu")

    # ── Logging ──────────────────────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv(
        "LOG_FORMAT", "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )


settings = Settings()
