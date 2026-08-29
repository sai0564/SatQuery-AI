# Git Workflow & Branching Guidelines

To support independent, modular development across teams without merge conflicts or architectural entanglement, SatQuery AI follows a strict feature-branch workflow.

---

## Branch Structure

| Branch | Purpose & Ownership |
| :--- | :--- |
| `main` | Production-ready baseline, protected branch. Merges only via Pull Requests. |
| `feature/geochat-agent` | GeoChat-7B single-image VQA, captioning, grounding prompts, and Colab integration. |
| `feature/changeformer-agent` | ChangeFormerV6 bi-temporal change detection model, Siamese feature extraction, and change masks. |
| `feature/optical-sar-agent` | BIFOLD RDNet multimodal fusion network for co-registered Optical + SAR imagery. |
| `feature/agent-router` | Agent task classification, dynamic routing, multi-step pipeline orchestration, and result integration. |
| `feature/backend` | FastAPI application, REST endpoints, request validation, authentication, and task queues. |
| `feature/frontend` | Web UI/dashboard, map viewer, split-screen change visualizer, and execution trace viewer. |
| `feature/evaluation` | Benchmark evaluation suites (VRSBench, RSVQA, CDVQA) and metric calculation scripts. |

---

## Development & PR Workflow

1. **Checkout Feature Branch**:
   ```bash
   git checkout feature/<your-feature-branch>
   git pull origin feature/<your-feature-branch>
   ```

2. **Develop Independently**:
   - Only modify files within your component's responsibility.
   - All specialist models must maintain the `BaseModelService.analyze(input_data, query)` interface.

3. **Run Verification & Tests**:
   ```bash
   pytest tests/
   ```

4. **Submit Pull Request**:
   - Open a PR into `main`.
   - Ensure automated CI/CD unit tests pass.
   - Code review and approval required before merging.
