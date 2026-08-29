"""
SatQuery AI - FastAPI Main Application Entrypoint.
Configures FastAPI app, CORS middleware, and mounts API router.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="SatQuery AI Backend",
        description="Agentic Vision-Language Assistant for Multimodal Remote-Sensing Image Analysis",
        version="0.1.0"
    )

    # Enable CORS for frontend integration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount API routes
    app.include_router(api_router)

    @app.get("/")
    def root():
        return {
            "message": "SatQuery AI API is running.",
            "docs": "/docs",
            "health": "/api/v1/health"
        }

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
