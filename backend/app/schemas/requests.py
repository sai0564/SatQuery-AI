"""
SatQuery AI — Request Schemas.

Typed request contract for the /analyze endpoint.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from backend.app.schemas.common import ImageModality


class ImageInput(BaseModel):
    """Metadata associated with an uploaded image.

    The actual file bytes are received via multipart form-data.
    This schema carries the structured metadata sent alongside.
    """

    filename: Optional[str] = None
    modality: ImageModality = ImageModality.OPTICAL
    capture_date: Optional[str] = Field(
        default=None, description="ISO-8601 date string, e.g. 2024-03-15"
    )


class AnalysisRequest(BaseModel):
    """JSON body for the /analyze endpoint.

    Images are uploaded as files via multipart form-data.
    The query and optional metadata come in a JSON part.
    """

    query: str = Field(
        default="Describe this image.",
        description="Natural-language question or instruction",
    )
    modality: Optional[ImageModality] = Field(
        default=None,
        description="Optional explicit modality hint (optical, sar)",
    )
    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Arbitrary key-value metadata (dates, sensor, location, etc.)",
    )
