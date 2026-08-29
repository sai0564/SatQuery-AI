"""
SatQuery AI — Model Registry.

A capability-aware registry that maps ``ModelCapability`` values to
concrete adapter instances. The router asks the registry:

    "Which adapter handles CHANGE_DETECTION?"

New models are registered at startup. The router never needs to be
rewritten when a model is added or swapped.
"""

from typing import Dict, List, Optional

from backend.app.models.base import BaseModelAdapter, ModelCapability
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)


class ModelRegistry:
    """Singleton-style registry of model adapters, keyed by capability."""

    def __init__(self) -> None:
        self._adapters: Dict[ModelCapability, BaseModelAdapter] = {}

    # ── Registration ─────────────────────────────────────────────

    def register(self, adapter: BaseModelAdapter) -> None:
        """Register an adapter for each capability it declares."""
        name = adapter.get_model_name()
        for cap in adapter.get_capabilities():
            self._adapters[cap] = adapter
            logger.info("Registered %s for capability %s", name, cap.value)

    # ── Lookup ───────────────────────────────────────────────────

    def get_adapter(self, capability: ModelCapability) -> Optional[BaseModelAdapter]:
        """Return the adapter registered for *capability*, or ``None``."""
        return self._adapters.get(capability)

    def has_capability(self, capability: ModelCapability) -> bool:
        return capability in self._adapters

    # ── Introspection ────────────────────────────────────────────

    def list_models(self) -> List[str]:
        """Return unique model names currently registered."""
        seen = set()
        names: List[str] = []
        for adapter in self._adapters.values():
            n = adapter.get_model_name()
            if n not in seen:
                seen.add(n)
                names.append(n)
        return names

    def list_capabilities(self) -> List[str]:
        """Return all registered capability values."""
        return [cap.value for cap in self._adapters]
