from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.db.session import get_db


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="BrandShield AI", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_error_handlers(app)

    @app.get("/api/v1/health")
    def health():
        return {"status": "ok", "service": "brandshield-api", "version": app.version}

    @app.get("/api/v1/health/db")
    def health_db(db: Session = Depends(get_db)):
        db.execute(text("SELECT 1"))
        has_vector = db.execute(
            text("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
        ).first()
        return {"status": "ok", "database": "connected", "pgvector": bool(has_vector)}

    return app


app = create_app()
