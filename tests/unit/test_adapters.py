"""
Unit tests for Model Adapters (Mocks & Base Interface).
Verifies that all mock outputs explicitly contain mock=True and confidence=None.
"""

from PIL import Image
from backend.app.models.base import AnalysisInput, ModelCapability
from backend.app.models.geochat.mock import GeoChatMockAdapter
from backend.app.models.changeformer.mock import ChangeFormerMockAdapter
from backend.app.models.bifold.mock import BifoldMockAdapter

def test_geochat_mock_adapter():
    adapter = GeoChatMockAdapter()
    assert adapter.get_model_name() == "GeoChat-7B (mock)"
    assert ModelCapability.SINGLE_IMAGE_VQA in adapter.get_capabilities()

    img = Image.new("RGB", (100, 100))
    inp = AnalysisInput(images=[img], query="What is in this image?")
    assert adapter.validate_input(inp) is None

    result = adapter.analyze(inp)
    assert result.mock is True
    assert result.confidence is None
    assert "GeoChat-7B" in result.answer
    assert "[MOCK]" in result.answer

def test_changeformer_mock_adapter():
    adapter = ChangeFormerMockAdapter()
    assert adapter.get_model_name() == "ChangeFormerV6 (mock)"
    assert ModelCapability.CHANGE_DETECTION in adapter.get_capabilities()

    img1 = Image.new("RGB", (100, 100))
    # Test invalid input (missing second image)
    invalid_inp = AnalysisInput(images=[img1], query="Compare")
    assert adapter.validate_input(invalid_inp) is not None

    img2 = Image.new("RGB", (100, 100))
    valid_inp = AnalysisInput(images=[img1, img2], query="Compare")
    assert adapter.validate_input(valid_inp) is None

    result = adapter.analyze(valid_inp)
    assert result.mock is True
    assert result.confidence is None
    assert len(result.evidence) > 0
    assert result.evidence[0]["type"] == "change_map"

def test_bifold_mock_adapter():
    adapter = BifoldMockAdapter()
    assert adapter.get_model_name() == "BIFOLD-RDNet (mock)"
    assert ModelCapability.OPTICAL_SAR_ANALYSIS in adapter.get_capabilities()

    img1 = Image.new("RGB", (100, 100))
    img2 = Image.new("RGB", (100, 100))
    inp = AnalysisInput(images=[img1, img2], query="Fuse optical and SAR")
    assert adapter.validate_input(inp) is None

    result = adapter.analyze(inp)
    assert result.mock is True
    assert result.confidence is None
    assert len(result.evidence) > 0
    assert result.evidence[0]["type"] == "fusion_result"
