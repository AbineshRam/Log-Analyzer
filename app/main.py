from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Log Analyzer",
        description="AI-powered job failure analysis and summarization",
        version="1.0.0",
    )

    # =========================
    # CORS (for GUI / browser)
    # =========================
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # =========================
    # API ROUTES
    # =========================
    app.include_router(api_router)

    # =========================
    # GUI (Static Web App)
    # =========================
    app.mount(
        "/",
        StaticFiles(directory="gui", html=True),
        name="gui",
    )

    return app


app = create_app()
