from fastapi import FastAPI
from src.routers import router as api_router
from src.core.config import get_settings
from src.core.exceptions import register_exception_handlers


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Real-Time Chat API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Routers
    app.include_router(api_router)

    # Exception handlers
    register_exception_handlers(app)

    return app


app = create_app()
