"""
SatQuery AI — Agent Router.

Orchestrates: classify → lookup adapter → validate → execute → evidence.

The router does NOT import concrete adapter classes. It only uses the
``ModelRegistry`` to find the right adapter by capability.
"""

import time
from typing import Any, Dict, List, Optional

from PIL import Image

from backend.app.agents.classifier import TaskClassifier
from backend.app.evidence.generator import EvidenceGenerator
from backend.app.models.base import AnalysisInput, AnalysisResult, ModelCapability
from backend.app.models.registry import ModelRegistry
from backend.app.schemas.common import AnalysisType, ImageModality
from backend.app.utils.errors import (
    ModelExecutionError,
    ModelUnavailableError,
    UnsupportedTaskError,
)
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)


class AgentRouter:
    """Routes analysis requests through the registered model adapters."""

    def __init__(self, registry: ModelRegistry) -> None:
        self.registry = registry

    def route(
        self,
        images: List[Image.Image],
        query: str,
        modality_hint: Optional[ImageModality] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Full routing pipeline.  Returns a dict ready to be wrapped in ``AnalysisResponse``."""
        trace: List[Dict[str, Any]] = []
        t0 = time.time()

        # ── 1. Classify ──────────────────────────────────────────
        analysis_type = TaskClassifier.classify(images, query, modality_hint, metadata)
        trace.append({"step": "classify", "analysis_type": analysis_type.value})
        logger.info("Classified task as %s", analysis_type.value)

        if analysis_type == AnalysisType.UNKNOWN:
            raise UnsupportedTaskError()

        # ── 2. Resolve capability → adapter ──────────────────────
        capability = TaskClassifier.analysis_type_to_capability(analysis_type)
        adapter = self.registry.get_adapter(capability)
        if adapter is None:
            raise ModelUnavailableError(capability.value)

        trace.append({
            "step": "adapter_selected",
            "model": adapter.get_model_name(),
            "capability": capability.value,
        })

        # ── 3. Validate input ────────────────────────────────────
        analysis_input = AnalysisInput(images=images, query=query, metadata=metadata or {})
        validation_error = adapter.validate_input(analysis_input)
        if validation_error:
            raise UnsupportedTaskError(validation_error)

        # ── 4. Execute ───────────────────────────────────────────
        try:
            result: AnalysisResult = adapter.analyze(analysis_input)
        except NotImplementedError as exc:
            raise ModelUnavailableError(capability.value) from exc
        except Exception as exc:
            raise ModelExecutionError(adapter.get_model_name(), str(exc)) from exc

        trace.append({"step": "model_executed", "model": result.model_name, "mock": result.mock})

        # ── 5. Evidence ──────────────────────────────────────────
        evidence_items = EvidenceGenerator.from_model_result(result.evidence)

        duration_ms = int((time.time() - t0) * 1000)
        trace.append({"step": "complete", "duration_ms": duration_ms})

        return {
            "analysis_type": analysis_type.value,
            "answer": result.answer,
            "model_used": result.model_name,
            "confidence": result.confidence,
            "mock": result.mock,
            "evidence": [e.model_dump() for e in evidence_items],
            "visual_outputs": result.visual_outputs,
            "metadata": result.metadata,
            "processing": {"duration_ms": duration_ms, "steps": trace},
            "errors": [],
        }
