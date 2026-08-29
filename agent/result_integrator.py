"""
Result Integrator for synthesizing specialist model outputs into standard response structure.
Synthesizes: Answer + Evidence + Confidence + Execution Trace.
"""

from typing import Any, Dict, List, Optional

class ResultIntegrator:
    @staticmethod
    def integrate(
        primary_result: Dict[str, Any],
        secondary_result: Optional[Dict[str, Any]] = None,
        execution_trace: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Integrates raw specialist outputs into a unified payload for the client/backend.
        """
        trace = execution_trace or []

        # If secondary_result exists (e.g. ChangeFormer -> GeoChat explanation pipeline)
        if secondary_result:
            answer = secondary_result.get("answer", primary_result.get("answer", ""))
            evidence = {
                "change_detection": primary_result.get("evidence", {}),
                "visual_explanation": secondary_result.get("evidence", {})
            }
            confidence = (primary_result.get("confidence", 0.9) + secondary_result.get("confidence", 0.9)) / 2.0
        else:
            answer = primary_result.get("answer", "No answer generated.")
            evidence = primary_result.get("evidence") or primary_result.get("grounding") or {}
            confidence = primary_result.get("confidence", 0.9)

        return {
            "answer": answer,
            "evidence": evidence,
            "confidence": round(confidence, 3),
            "execution_trace": trace,
            "metadata": {
                "status": "success",
                "primary_model": primary_result.get("model", "unknown"),
                "secondary_model": secondary_result.get("model") if secondary_result else None
            }
        }
