# SatQuery AI - Architecture Documentation

## Overview
**SatQuery AI** is an agentic vision-language assistant for multimodal remote-sensing image analysis. The system orchestrates multiple specialized models to answer questions, detect change over time, and fuse optical and Synthetic Aperture Radar (SAR) imagery.

---

## Agent Flow & Routing Pipeline

```
Frontend (User Input: Image(s) + Query)
   ↓
FastAPI Backend (/api/v1/analyze)
   ↓
Input Validation (preprocessing/image_validator.py)
   ↓
Agent Router (agent/router.py & agent/task_classifier.py)
   ↓
Specialist Model Selection & Execution
   ├── 1. Single Image → GeoChat-7B (models/geochat/)
   ├── 2. Bi-temporal Pair → ChangeFormerV6 (models/changeformer/)
   │                           ↓
   │                      GeoChat-7B (Explain detected changes)
   └── 3. Optical + SAR Pair → BIFOLD RDNet (models/bifold/)
   ↓
Result Integrator (agent/result_integrator.py)
   ↓
Unified Output: Answer + Evidence + Confidence + Execution Trace
   ↓
Frontend Client
```

---

## Specialist Models & Responsibilities

| Model | Architecture | Primary Task | Input | Output |
| :--- | :--- | :--- | :--- | :--- |
| **GeoChat-7B** | LLaVA-based LVLM | Single-image VQA, scene captioning, spatial grounding | 1 Optical Image + Query | Text answer, bounding boxes |
| **ChangeFormerV6** | Siamese Transformer | Bi-temporal change detection | Image $T_1$ & Image $T_2$ | Change map, change ratio, bounding boxes |
| **BIFOLD RDNet** | Dual-Branch Fusion Net | Co-registered Optical + SAR analysis | Optical Image + SAR Image | Fused targets, penetration evidence |

---

## Unified Model Interface
To enforce modularity and allow independent deployment or replacement of any model, each model adheres to `BaseModelService`:

```python
class BaseModelService(ABC):
    @abstractmethod
    def analyze(self, input_data: Dict[str, Any], query: Optional[str] = None) -> Dict[str, Any]:
        pass
```
