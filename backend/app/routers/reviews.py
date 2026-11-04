
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import ContentAudit
from app.routers.guidelines import get_default_organisation

router = APIRouter(
    prefix="/api/v1/reviews",
    tags=["Human Reviews"],
)


class ReviewDecision(BaseModel):
    decision: str = Field(
        description="approve, reject, or request_changes"
    )
    reviewer_comment: str = Field(
        default="",
        max_length=2000,
    )


@router.get("")
def list_audits(
    db: Session = Depends(get_db),
):
    organisation = get_default_organisation(db)

    audits = db.scalars(
        select(ContentAudit)
        .where(
            ContentAudit.organisation_id == organisation.id
        )
        .order_by(ContentAudit.created_at.desc())
    ).all()

    return [
        {
            "id": str(audit.id),
            "submitted_content": audit.submitted_content,
            "overall_status": audit.overall_status,
            "summary": audit.summary,
            "findings": audit.findings,
            "review_status": audit.review_status,
            "created_at": audit.created_at,
        }
        for audit in audits
    ]


@router.get("/{audit_id}")
def get_audit(
    audit_id: UUID,
    db: Session = Depends(get_db),
):
    organisation = get_default_organisation(db)

    audit = db.scalar(
        select(ContentAudit).where(
            ContentAudit.id == audit_id,
            ContentAudit.organisation_id == organisation.id,
        )
    )

    if audit is None:
        raise HTTPException(
            status_code=404,
            detail="Audit not found.",
        )

    return {
        "id": str(audit.id),
        "submitted_content": audit.submitted_content,
        "overall_status": audit.overall_status,
        "summary": audit.summary,
        "findings": audit.findings,
        "review_status": audit.review_status,
        "created_at": audit.created_at,
    }


@router.patch("/{audit_id}/decision")
def review_audit(
    audit_id: UUID,
    request: ReviewDecision,
    db: Session = Depends(get_db),
):
    organisation = get_default_organisation(db)

    audit = db.scalar(
        select(ContentAudit).where(
            ContentAudit.id == audit_id,
            ContentAudit.organisation_id == organisation.id,
        )
    )

    if audit is None:
        raise HTTPException(
            status_code=404,
            detail="Audit not found.",
        )

    allowed_decisions = [
        "approve",
        "reject",
        "request_changes",
    ]

    if request.decision not in allowed_decisions:
        raise HTTPException(
            status_code=400,
            detail="Invalid decision. Use approve, reject, or request_changes.",
        )

    audit.review_status = request.decision
    db.commit()
    db.refresh(audit)

    return {
        "message": "Review decision saved successfully.",
        "audit_id": str(audit.id),
        "review_status": audit.review_status,
        "reviewer_comment": request.reviewer_comment,
    }

