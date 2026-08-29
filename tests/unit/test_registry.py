"""
Unit tests for ModelRegistry.
"""

from backend.app.models.registry import ModelRegistry
from backend.app.models.base import ModelCapability
from backend.app.models.geochat.mock import GeoChatMockAdapter
from backend.app.models.changeformer.mock import ChangeFormerMockAdapter

def test_registry_registration_and_lookup():
    registry = ModelRegistry()
    geochat = GeoChatMockAdapter()
    registry.register(geochat)

    assert registry.has_capability(ModelCapability.SINGLE_IMAGE_VQA)
    assert registry.get_adapter(ModelCapability.SINGLE_IMAGE_VQA) is geochat
    assert not registry.has_capability(ModelCapability.CHANGE_DETECTION)

    changeformer = ChangeFormerMockAdapter()
    registry.register(changeformer)
    assert registry.has_capability(ModelCapability.CHANGE_DETECTION)
    assert registry.get_adapter(ModelCapability.CHANGE_DETECTION) is changeformer

def test_registry_list_models():
    registry = ModelRegistry()
    registry.register(GeoChatMockAdapter())
    registry.register(ChangeFormerMockAdapter())

    models = registry.list_models()
    assert "GeoChat-7B (mock)" in models
    assert "ChangeFormerV6 (mock)" in models
