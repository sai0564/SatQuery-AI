"""
Unit tests for EvidenceGenerator.
"""

from backend.app.evidence.generator import EvidenceGenerator
from backend.app.schemas.common import EvidenceItem

def test_evidence_generator():
    raw_evidence = [
        {
            "type": "change_map",
            "description": "Significant changes detected",
            "bounding_boxes": [
                {"label": "new_building", "x_min": 10, "y_min": 20, "x_max": 50, "y_max": 80, "confidence": 0.88}
            ],
            "metadata": {"ratio": 0.15}
        }
    ]

    items = EvidenceGenerator.from_model_result(raw_evidence)
    assert len(items) == 1
    item = items[0]
    assert isinstance(item, EvidenceItem)
    assert item.type == "change_map"
    assert len(item.bounding_boxes) == 1
    assert item.bounding_boxes[0].label == "new_building"
    assert item.bounding_boxes[0].x_min == 10
    assert item.metadata["ratio"] == 0.15
