from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    database_url: str = "postgresql+psycopg://brandshield:brandshield@localhost:5432/brandshield"
    jwt_secret: str = "dev-only-insecure-secret"
    jwt_expire_minutes: int = 60
    cors_origins: str = "http://localhost:5173"
    max_upload_mb: int = 10
    storage_backend: str = "local"
    storage_local_dir: str = "./storage"

    ai_provider: str = "gemini"
    gemini_api_key: str = ""
    openai_api_key: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if settings.environment == "production" and settings.jwt_secret == "dev-only-insecure-secret":
        raise RuntimeError("JWT_SECRET must be set in production")
    return settings
