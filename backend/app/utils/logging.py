"""
SatQuery AI — Logging Configuration.

Provides a configured logger for the application.
"""

import logging
import sys

from backend.app.config.settings import settings


def get_logger(name: str) -> logging.Logger:
    """Return a logger with consistent formatting."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
        logger.addHandler(handler)

    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    return logger
