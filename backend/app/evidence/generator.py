"""
SatQuery AI — Evidence Generator.

Creates structured evidence items from model outputs.
Independent from the frontend — evidence is data, not HTML.
"""

from typing import Any, Dict, List

from backend.app.schemas.common import BoundingBox, EvidenceItem


class EvidenceGenerator:
    """Creates evidence payloads from raw model outputs."""

    @staticmethod
    def from_model_result(
        raw_evidence: List[Dict[str, Any]],
    ) -> List[EvidenceItem]:
        """Convert adapter evidence dicts into typed EvidenceItem objects."""
        items: List[EvidenceItem] = []
        for raw in raw_evidence:
            boxes = []
            for b in raw.get("bounding_boxes", []):
                boxes.append(
                    BoundingBox(
                        label=b.get("label", ""),
                        x_min=b.get("x_min", 0),
                        y_min=b.get("y_min", 0),
                        x_max=b.get("x_max", 0),
                        y_max=b.get("y_max", 0),
                        confidence=b.get("confidence"),
                    )
                )
            items.append(
                EvidenceItem(
                    type=raw.get("type", "unknown"),
                    description=raw.get("description", ""),
                    image_path=raw.get("image_path"),
                    mask_path=raw.get("mask_path"),
                    bounding_boxes=boxes,
                    metadata=raw.get("metadata", {}),
                )
            )
        return items
