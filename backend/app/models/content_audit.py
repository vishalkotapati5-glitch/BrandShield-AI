
import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdTimestampMixin


class ContentAudit(IdTimestampMixin, Base):
    __tablename__ = "content_audits"

    organisation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    submitted_content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    overall_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    findings: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    review_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pending",
    )
