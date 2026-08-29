# SatQuery AI — Model Integration Guide

This guide explains how to replace development **Mock Adapters** with **Real Model Adapters** as model integration branches mature.

---

## Adapter Replacement Architecture

```
                      BaseModelAdapter (Interface)
                                   ▲
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         │                                                   │
  GeoChatMockAdapter                                   GeoChatAdapter
  (mock=True, confidence=None)                         (Real PyTorch weights / Remote API)
```

---

## Step-by-Step Integration

### 1. GeoChat-7B Integration (on `feature/geochat-agent`)
1. Implement real inference loading in `backend/app/models/geochat/adapter.py`.
2. Connect to GPU or remote Colab / Cloud inference endpoint.
3. In `backend/app/api/dependencies.py`:
   ```python
   # Swap registration
   from backend.app.models.geochat.adapter import GeoChatAdapter
   registry.register(GeoChatAdapter())
   ```
4. Note: If the real model does not output a calibrated confidence score, return `confidence=None` (do not fabricate scores).

---

### 2. ChangeFormerV6 Integration (on `feature/changeformer-agent`)
1. Implement Siamese feature extraction and change mask thresholding in `backend/app/models/changeformer/adapter.py`.
2. Generate binary change mask arrays and extract connected component bounding boxes.
3. In `backend/app/api/dependencies.py`:
   ```python
   from backend.app.models.changeformer.adapter import ChangeFormerAdapter
   registry.register(ChangeFormerAdapter())
   ```

---

### 3. BIFOLD RDNet Integration (on `feature/optical-sar-agent`)
1. Implement dual-branch Optical + SAR encoder in `backend/app/models/bifold/adapter.py`.
2. Pass co-registered Optical and SAR tensor pairs through fusion layers.
3. In `backend/app/api/dependencies.py`:
   ```python
   from backend.app.models.bifold.adapter import BifoldAdapter
   registry.register(BifoldAdapter())
   ```
