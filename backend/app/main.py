
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.db.session import get_db
from app.routers.guidelines import router as guidelines_router
from app.routers.audits import router as audits_router
from app.routers.reviews import router as reviews_router


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="BrandShield AI",
        description="AI-powered brand governance and content auditing platform",
        version="0.1.0",
    )

    # Configure frontend access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register application error handlers
    register_error_handlers(app)
    app.include_router(guidelines_router)
    app.include_router(audits_router)
    app.include_router(reviews_router)

    # Basic API health check
    @app.get("/api/v1/health", tags=["Health"])
    def health():
        return {
            "status": "ok",
            "service": "brandshield-api",
            "version": app.version,
        }

    # Database health check
    @app.get("/api/v1/health/db", tags=["Health"])
    def health_db(db: Session = Depends(get_db)):
        db.execute(text("SELECT 1"))

        has_vector = db.execute(
            text(
                "SELECT 1 FROM pg_extension "
                "WHERE extname = 'vector'"
            )
        ).first()

        return {
            "status": "ok",
            "database": "connected",
            "pgvector": bool(has_vector),
        }

    return app


app = create_app()
