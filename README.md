# SatQuery AI 🛰️🤖

**SatQuery AI** is an agentic vision-language assistant designed for multimodal remote-sensing image analysis. It unifies specialized deep learning models under an intelligent agent router to handle visual question answering, bi-temporal change detection, and optical-SAR feature fusion.

---

## 🏛️ Project Architecture

```
SatQuery-AI/
├── backend/                  # FastAPI Application & REST API
│   ├── main.py               # App entrypoint & CORS
│   ├── api/                  # Routes & Pydantic schemas
│   │   ├── routes.py
│   │   └── schemas.py
│   └── services/             # Agent orchestration service
│       └── agent_service.py
│
├── agent/                    # Intelligent Routing & Synthesis Engine
│   ├── router.py             # Model dispatching & multi-step execution
│   ├── task_classifier.py    # Intent & modality classification
│   └── result_integrator.py  # Response, evidence, and trace synthesizer
│
├── models/                   # Specialist Model Implementations
│   ├── base.py               # Unified BaseModelService abstract interface
│   ├── geochat/              # GeoChat-7B (Single-image VQA & Captioning)
│   │   ├── inference.py
│   │   └── service.py
│   ├── changeformer/         # ChangeFormerV6 (Bi-temporal change detection)
│   │   ├── inference.py
│   │   └── service.py
│   └── bifold/               # BIFOLD RDNet (Optical + SAR multimodal fusion)
│       ├── inference.py
│       └── service.py
│
├── preprocessing/            # Input validation & sensor data preprocessors
│   ├── image_validator.py    # Dimensions, channels, & metadata verification
│   ├── optical.py            # Optical normalizer
│   ├── sar.py                # SAR calibration & speckle filtering
│   └── temporal.py           # Resolution & bounding-box alignment
│
├── evaluation/               # Benchmark evaluation pipelines
│   ├── vrsbench/             # VRSBench
│   ├── rsvqa/                # RSVQA
│   └── cdvqa/                # CDVQA
│
├── frontend/                 # Client UI & visualization dashboard
├── tests/                    # Unit and integration test suite
├── docs/                     # Architecture & workflow documentation
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

---

## 🧭 Agent Flow & Routing Logic

1. **Single Image** $\rightarrow$ **GeoChat-7B** (VQA, captioning, grounded scene understanding).
2. **Two Images ($T_1, T_2$)** $\rightarrow$ **ChangeFormerV6** (generates change mask and metrics) $\rightarrow$ **GeoChat-7B** (explains detected changes in plain language).
3. **Optical + SAR Pair** $\rightarrow$ **BIFOLD RDNet** (co-registered multimodal feature fusion and structure detection).

### Result Output Structure
Each query returns:
- **`answer`**: Natural language response to the user's question.
- **`evidence`**: Bounding boxes, change ratio, or radar indicators.
- **`confidence`**: Estimated confidence score ($0.0 - 1.0$).
- **`execution_trace`**: Detailed audit trail of routing decisions and model activations.

---

## 🚀 Quick Start

### 1. Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the FastAPI Backend
```bash
uvicorn backend.main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/v1/health`

### 3. Run Automated Tests
```bash
pytest tests/
```

---

## 🌿 Git Branching Strategy

| Branch | Focus |
| :--- | :--- |
| `main` | Production baseline (protected) |
| `feature/geochat-agent` | GeoChat-7B integration |
| `feature/changeformer-agent` | ChangeFormerV6 integration |
| `feature/optical-sar-agent` | BIFOLD RDNet integration |
| `feature/agent-router` | Agent routing & classifier logic |
| `feature/backend` | API endpoints & service layer |
| `feature/frontend` | Dashboard UI |
| `feature/evaluation` | Benchmark evaluation suites |
