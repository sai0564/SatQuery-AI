"""
Unit tests for TaskClassifier.
"""

from PIL import Image
from backend.app.agents.classifier import TaskClassifier
from backend.app.models.base import ModelCapability
from backend.app.schemas.common import AnalysisType, ImageModality

def test_classify_empty_images():
    task = TaskClassifier.classify([], query="What is here?")
    assert task == AnalysisType.UNKNOWN

def test_classify_single_image():
    img = Image.new("RGB", (100, 100))
    task = TaskClassifier.classify([img], query="Describe this satellite scene.")
    assert task == AnalysisType.SINGLE_IMAGE_VQA

def test_classify_two_images_change_detection():
    img1 = Image.new("RGB", (100, 100))
    img2 = Image.new("RGB", (100, 100))
    task = TaskClassifier.classify([img1, img2], query="Compare these two dates.")
    assert task == AnalysisType.CHANGE_DETECTION

def test_classify_optical_sar_pair():
    img1 = Image.new("RGB", (100, 100))
    img2 = Image.new("RGB", (100, 100))
    task = TaskClassifier.classify(
        [img1, img2],
        query="Analyze optical and SAR data.",
        modality_hint=ImageModality.SAR
    )
    assert task == AnalysisType.OPTICAL_SAR_ANALYSIS

def test_capability_mapping():
    assert TaskClassifier.analysis_type_to_capability(AnalysisType.SINGLE_IMAGE_VQA) == ModelCapability.SINGLE_IMAGE_VQA
    assert TaskClassifier.analysis_type_to_capability(AnalysisType.CHANGE_DETECTION) == ModelCapability.CHANGE_DETECTION
    assert TaskClassifier.analysis_type_to_capability(AnalysisType.OPTICAL_SAR_ANALYSIS) == ModelCapability.OPTICAL_SAR_ANALYSIS
