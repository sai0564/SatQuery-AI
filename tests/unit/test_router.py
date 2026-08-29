"""
Unit tests for AgentRouter.
"""

from PIL import Image
from backend.app.agents.router import AgentRouter
from backend.app.models.registry import ModelRegistry
from backend.app.models.geochat.mock import GeoChatMockAdapter
from backend.app.models.changeformer.mock import ChangeFormerMockAdapter
from backend.app.models.bifold.mock import BifoldMockAdapter
from backend.app.schemas.common import ImageModality
from backend.app.utils.errors import UnsupportedTaskError, ModelUnavailableError

def create_populated_router():
    registry = ModelRegistry()
    registry.register(GeoChatMockAdapter())
    registry.register(ChangeFormerMockAdapter())
    registry.register(BifoldMockAdapter())
    return AgentRouter(registry=registry)

def test_router_single_image():
    router = create_populated_router()
    img = Image.new("RGB", (100, 100))
    res = router.route(images=[img], query="What is in this image?")
    assert res["analysis_type"] == "SINGLE_IMAGE_VQA"
    assert res["mock"] is True
    assert res["confidence"] is None
    assert "GeoChat-7B" in res["model_used"]
    assert len(res["processing"]["steps"]) > 0

def test_router_bitemporal():
    router = create_populated_router()
    img1 = Image.new("RGB", (100, 100))
    img2 = Image.new("RGB", (100, 100))
    res = router.route(images=[img1, img2], query="Compare changes.")
    assert res["analysis_type"] == "CHANGE_DETECTION"
    assert res["mock"] is True
    assert "ChangeFormerV6" in res["model_used"]
    assert len(res["evidence"]) > 0

def test_router_optical_sar():
    router = create_populated_router()
    img1 = Image.new("RGB", (100, 100))
    img2 = Image.new("RGB", (100, 100))
    res = router.route(
        images=[img1, img2],
        query="Detect vessels.",
        modality_hint=ImageModality.SAR
    )
    assert res["analysis_type"] == "OPTICAL_SAR_ANALYSIS"
    assert res["mock"] is True
    assert "BIFOLD-RDNet" in res["model_used"]

def test_router_empty_images():
    router = create_populated_router()
    try:
        router.route(images=[], query="Describe.")
        assert False, "Expected UnsupportedTaskError"
    except UnsupportedTaskError:
        pass

def test_router_missing_model_for_capability():
    empty_registry = ModelRegistry()
    router = AgentRouter(registry=empty_registry)
    img = Image.new("RGB", (100, 100))
    try:
        router.route(images=[img], query="Describe.")
        assert False, "Expected ModelUnavailableError"
    except ModelUnavailableError:
        pass
