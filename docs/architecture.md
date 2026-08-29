# SatQuery AI — Architecture Documentation

## 1. System Overview

**SatQuery AI** is a production-quality satellite image analysis platform. It provides an agentic vision-language assistant for multimodal remote-sensing image analysis, supporting:
- Single-image satellite visual question answering (VQA) & scene captioning
- Bi-temporal change detection & change-map generation
- Optical + Synthetic Aperture Radar (SAR) multimodal fusion analysis

---

## 2. Core Architecture & Data Flow

```
                      React / TypeScript Frontend
                                  │ (Multipart Upload + Query)
                                  ▼
                            FastAPI Backend
                                  │
                                  ▼
                          Analysis Service
                                  │
                                  ▼
                           Image Validator
                        (Format, Bounds, Decode)
                                  │
                                  ▼
                           AI Agent Router
                                  │ (Query & Input Inspection)
                                  ▼
                            Model Registry
                       (Capability-based lookup)
                                  │
                ┌─────────────────┼─────────────────┐
                ▼                 ▼                 ▼
          GeoChatAdapter   ChangeFormerAdapter  BifoldAdapter
          (SINGLE_IMAGE)   (CHANGE_DETECTION)   (OPTICAL_SAR)
                │                 │                 │
           GeoChat-7B       ChangeFormerV6     BIFOLD RDNet
                │                 │                 │
                └─────────────────┼─────────────────┘
                                  ▼
                          Evidence Generator
                      (Overlays, BBoxes, Masks)
                                  │
                                  ▼
                      Structured AnalysisResult
                                  │
                                  ▼
                            FastAPI Return
                                  │
                                  ▼
                             Frontend UI
```

---

## 3. Key Architectural Principles

1. **Strict Model Decoupling (`BaseModelAdapter`)**:
   - The router communicates **only** with model adapters via `analyze(analysis_input) -> AnalysisResult`.
   - The router never imports model-specific deep learning frameworks or internal checkpoints.
   - All models declare their capabilities (`ModelCapability.SINGLE_IMAGE_VQA`, `ModelCapability.CHANGE_DETECTION`, etc.).

2. **Model Registry**:
   - Manages available adapters by capability.
   - New models or alternative backends can be registered at runtime without touching router code.

3. **Explicit Mock Representation**:
   - During local development or on CPU environments, mock adapters return responses marked with `"mock": true` and `"confidence": null`.
   - Mock outputs are never presented as real model inferences.

4. **Structured Evidence Pipeline**:
   - Evidence items (bounding boxes, change ratios, radar penetration indicators, heatmaps) are structured as data objects independent of frontend visualization logic.

5. **Storage Abstraction**:
   - `StorageService` encapsulates local filesystem storage for development and can be swapped for S3/GCS/Azure Blob in cloud production deployments.
