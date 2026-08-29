# Unit tests for AgentRouter, TaskClassifier, and ResultIntegrator.
from agent.task_classifier import TaskClassifier, TaskType
from agent.router import AgentRouter
from agent.result_integrator import ResultIntegrator

def test_task_classification():
    # Test single image classification
    assert TaskClassifier.classify({"image": "sample_img"}) == TaskType.SINGLE_IMAGE_VQA_CAPTION

    # Test bi-temporal classification
    assert TaskClassifier.classify({"image_t1": "t1_img", "image_t2": "t2_img"}) == TaskType.CHANGE_DETECTION_EXPLANATION

    # Test optical + SAR classification
    assert TaskClassifier.classify({"optical_image": "opt_img", "sar_image": "sar_img"}) == TaskType.OPTICAL_SAR_FUSION

    # Test unknown input
    assert TaskClassifier.classify({}) == TaskType.UNKNOWN

def test_single_image_routing():
    router = AgentRouter()
    result = router.route_and_execute({"image": "satellite.png"}, query="What is in this image?")
    
    assert "answer" in result
    assert result["metadata"]["primary_model"] == "GeoChat-7B"
    assert result["confidence"] > 0
    assert len(result["execution_trace"]) >= 2
    assert result["execution_trace"][0]["step"] == "task_classification"

def test_bitemporal_routing():
    router = AgentRouter()
    result = router.route_and_execute(
        {"image_t1": "date1.png", "image_t2": "date2.png"},
        query="What changed between these two dates?"
    )

    assert "answer" in result
    assert result["metadata"]["primary_model"] == "ChangeFormerV6"
    assert result["metadata"]["secondary_model"] == "GeoChat-7B"
    assert "change_detection" in result["evidence"]
    assert len(result["execution_trace"]) >= 3

def test_optical_sar_routing():
    router = AgentRouter()
    result = router.route_and_execute(
        {"optical_image": "opt.png", "sar_image": "sar.png"},
        query="Detect vessels under cloud cover."
    )

    assert "answer" in result
    assert result["metadata"]["primary_model"] == "BIFOLD-RDNet"
    assert "detected_targets" in result["evidence"]
    assert len(result["execution_trace"]) >= 2
