# SatQuery AI — Setup & Local Development Guide

## Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- Git
- Docker & Docker Compose (optional for containerized execution)

---

## 1. Local Python Setup

```bash
# Clone repository
git clone https://github.com/sai0564/SatQuery-AI.git
cd SatQuery-AI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

---

## 2. Running the Backend

```bash
uvicorn backend.app.main:app --reload --port 8000
```
- API Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

---

## 3. Running with Docker

```bash
# From workspace root
docker compose -f docker/docker-compose.yml up --build
```

---

## 4. Running the Test Suite

```bash
pytest tests/
```
