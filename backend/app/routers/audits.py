
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import BrandGuideline, ContentAudit
from app.routers.guidelines import get_default_organisation
from app.schemas.audit import AuditRequest, AuditResponse
from app.services.audit_service import audit_content

router = APIRouter(
    prefix="/api/v1/audits",
    tags=["Content Audits"],
)


@router.post("", response_model=AuditResponse)
def create_audit(
    request: AuditRequest,
    db: Session = Depends(get_db),
):
    organisation = get_default_organisation(db)

    guidelines = db.scalars(
        select(BrandGuideline).where(
            BrandGuideline.organisation_id == organisation.id,
            BrandGuideline.is_active.is_(True),
        )
    ).all()

    if not guidelines:
        raise HTTPException(
            status_code=400,
            detail="No active brand guidelines found. Add guidelines first.",
        )

    guideline_data = [
        {
            "title": guideline.title,
            "category": guideline.category,
            "rule": guideline.rule,
        }
        for guideline in guidelines
    ]

    try:
        result = audit_content(
            content=request.content,
            guidelines=guideline_data,
        )

        audit_record = ContentAudit(
            organisation_id=organisation.id,
            submitted_content=request.content,
            overall_status=result["overall_status"],
            summary=result["summary"],
            findings=result["findings"],
            review_status="pending",
        )

        db.add(audit_record)
        db.commit()
        db.refresh(audit_record)

        return result

    except Exception as exc:
        db.rollback()
        print(f"Audit service error: {type(exc).__name__}: {exc}")

        raise HTTPException(
            status_code=502,
            detail="The AI audit could not be completed. Please try again.",
        ) from exc
