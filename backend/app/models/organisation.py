import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdTimestampMixin


class Organisation(IdTimestampMixin, Base):
    __tablename__ = "organisations"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    # External AI is OFF by default; enabling requires admin consent (recorded below).
    external_ai_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # FK to users is added in Stage 1 once the users table exists.
    ai_consent_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    ai_consent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
