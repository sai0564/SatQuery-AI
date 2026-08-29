"""
SatQuery AI — FastAPI Application Entrypoint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.analysis import router as analysis_router
from backend.app.config.settings import settings
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="Agentic Vision-Language Assistant for Multimodal Remote-Sensing Image Analysis",
        version=settings.APP_VERSION,
    )

    # ── CORS ─────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routes ───────────────────────────────────────────────────
    app.include_router(analysis_router)

    @app.get("/")
    def root():
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": f"{settings.API_PREFIX}/health",
        }

    # ── Startup ──────────────────────────────────────────────────
    @app.on_event("startup")
    async def startup():
        # Ensure upload / evidence dirs exist
        settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        settings.EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(
            "%s v%s started (mock_mode=%s)",
            settings.APP_NAME,
            settings.APP_VERSION,
            settings.USE_MOCK_MODELS,
        )

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
