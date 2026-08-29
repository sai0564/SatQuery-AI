"""
SatQuery AI — Analysis Service.

Orchestrates: file validation → image decoding → routing → response.
This is the single entry-point called by the API route.
"""

import uuid
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image

from backend.app.agents.router import AgentRouter
from backend.app.image_processing.validator import validate_file
from backend.app.schemas.common import ImageModality
from backend.app.utils.errors import MissingImageError, SatQueryError
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)


class AnalysisService:
    """High-level service consumed by the API layer."""

    def __init__(self, router: AgentRouter) -> None:
        self.router = router

    async def analyze(
        self,
        files: List[Tuple[str, bytes]],  # [(filename, raw_bytes), ...]
        query: str = "Describe this image.",
        modality_hint: Optional[ImageModality] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Run the full analysis pipeline and return a response dict."""
        request_id = uuid.uuid4().hex

        # ── Validate & decode images ─────────────────────────────
        if not files:
            raise MissingImageError()

        images: List[Image.Image] = []
        for filename, raw in files:
            img = validate_file(raw, filename)
            images.append(img)

        logger.info(
            "Request %s: %d image(s), query='%s'",
            request_id,
            len(images),
            query[:80],
        )

        # ── Route ────────────────────────────────────────────────
        result = self.router.route(
            images=images,
            query=query,
            modality_hint=modality_hint,
            metadata=metadata,
        )

        result["request_id"] = request_id
        return result
