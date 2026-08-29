"""
SatQuery AI — API Dependencies.

Provides shared instances (registry, router, service) via FastAPI's
dependency injection system.
"""

from functools import lru_cache

from backend.app.agents.router import AgentRouter
from backend.app.config.settings import settings
from backend.app.models.bifold.mock import BifoldMockAdapter
from backend.app.models.changeformer.mock import ChangeFormerMockAdapter
from backend.app.models.geochat.mock import GeoChatMockAdapter
from backend.app.models.registry import ModelRegistry
from backend.app.services.analysis_service import AnalysisService


@lru_cache()
def get_registry() -> ModelRegistry:
    """Build and populate the model registry once."""
    registry = ModelRegistry()

    if settings.USE_MOCK_MODELS:
        registry.register(GeoChatMockAdapter())
        registry.register(ChangeFormerMockAdapter())
        registry.register(BifoldMockAdapter())
    else:
        # When real models are integrated, register real adapters here
        # from backend.app.models.geochat.adapter import GeoChatAdapter
        # registry.register(GeoChatAdapter())
        pass

    return registry


def get_router() -> AgentRouter:
    return AgentRouter(registry=get_registry())


def get_analysis_service() -> AnalysisService:
    return AnalysisService(router=get_router())
