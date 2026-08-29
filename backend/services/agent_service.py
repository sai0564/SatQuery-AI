"""
Agent Service Orchestrator for FastAPI.
Validates incoming payload, invokes AgentRouter, and shapes the final response.
"""

from typing import Any, Dict
from agent.router import AgentRouter
from preprocessing.image_validator import ImageValidator

class AgentService:
    def __init__(self, router: AgentRouter = None):
        self.router = router or AgentRouter()

    def process_analysis_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates request and routes to agent workflow.
        """
        query = payload.get("query")
        
        # Check validation if applicable
        if payload.get("image"):
            is_valid, err = ImageValidator.validate_single_image(payload["image"])
            if not is_valid:
                return {
                    "answer": f"Validation failed: {err}",
                    "evidence": {},
                    "confidence": 0.0,
                    "execution_trace": [{"step": "validation_error", "message": err}],
                    "metadata": {"status": "error"}
                }

        # Execute routing and integration
        return self.router.route_and_execute(input_data=payload, query=query)
