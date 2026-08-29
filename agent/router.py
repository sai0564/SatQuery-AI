"""
Agent Router for SatQuery AI.
Orchestrates model selection, multi-step pipeline execution, and trace logging.
"""

from typing import Any, Dict, List, Optional
import time

from agent.task_classifier import TaskClassifier, TaskType
from agent.result_integrator import ResultIntegrator
from models.geochat.service import GeoChatService
from models.changeformer.service import ChangeFormerService
from models.bifold.service import BifoldService

class AgentRouter:
    def __init__(
        self,
        geochat_service: Optional[GeoChatService] = None,
        changeformer_service: Optional[ChangeFormerService] = None,
        bifold_service: Optional[BifoldService] = None
    ):
        self.geochat = geochat_service or GeoChatService()
        self.changeformer = changeformer_service or ChangeFormerService()
        self.bifold = bifold_service or BifoldService()

    def route_and_execute(self, input_data: Dict[str, Any], query: Optional[str] = None) -> Dict[str, Any]:
        """
        Routes the user request to the appropriate specialist model(s) and integrates the results.
        """
        execution_trace: List[Dict[str, Any]] = []
        start_time = time.time()

        # Step 1: Task Classification
        task_type = TaskClassifier.classify(input_data, query)
        execution_trace.append({
            "step": "task_classification",
            "task_type": task_type.value,
            "timestamp": time.time()
        })

        if task_type == TaskType.SINGLE_IMAGE_VQA_CAPTION:
            # Single Image -> GeoChat-7B
            execution_trace.append({
                "step": "model_dispatch",
                "model": "GeoChat-7B",
                "action": "Single-image VQA / Captioning"
            })
            primary_res = self.geochat.analyze(input_data, query)
            return ResultIntegrator.integrate(primary_result=primary_res, execution_trace=execution_trace)

        elif task_type == TaskType.CHANGE_DETECTION_EXPLANATION:
            # Two images -> ChangeFormerV6 -> GeoChat-7B for explanation
            execution_trace.append({
                "step": "model_dispatch",
                "model": "ChangeFormerV6",
                "action": "Bi-temporal change detection"
            })
            change_res = self.changeformer.analyze(input_data, query)

            execution_trace.append({
                "step": "model_dispatch",
                "model": "GeoChat-7B",
                "action": "Change explanation generation"
            })
            # Prepare contextualized prompt for GeoChat based on change results
            explanation_query = f"Explain the remote sensing changes detected: {change_res['answer']}. Query: {query or 'What changed?'}"
            explanation_input = {"image": input_data.get("image_t2") or input_data.get("image_t1")}
            geochat_res = self.geochat.analyze(explanation_input, explanation_query)

            return ResultIntegrator.integrate(
                primary_result=change_res,
                secondary_result=geochat_res,
                execution_trace=execution_trace
            )

        elif task_type == TaskType.OPTICAL_SAR_FUSION:
            # Optical + SAR pair -> BIFOLD RDNet
            execution_trace.append({
                "step": "model_dispatch",
                "model": "BIFOLD-RDNet",
                "action": "Multimodal Optical + SAR feature fusion"
            })
            fusion_res = self.bifold.analyze(input_data, query)
            return ResultIntegrator.integrate(primary_result=fusion_res, execution_trace=execution_trace)

        else:
            execution_trace.append({
                "step": "error",
                "message": "Unsupported or unrecognized input modality configuration."
            })
            return {
                "answer": "Unable to process request: Unrecognized input format or missing images.",
                "evidence": {},
                "confidence": 0.0,
                "execution_trace": execution_trace,
                "metadata": {"status": "error"}
            }
