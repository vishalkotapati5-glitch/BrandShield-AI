
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import BrandGuideline, Organisation
from app.schemas.brand_guideline import (
    BrandGuidelineCreate,
    BrandGuidelineResponse,
    BrandGuidelineUpdate,
)

router = APIRouter(
    prefix="/api/v1/guidelines",
    tags=["Brand Guidelines"],
)


def get_default_organisation(db: Session) -> Organisation:
    """
    Temporary single-organisation setup for the MVP.
    Authentication and organisation selection will be added later.
    """
    organisation = db.scalar(
        select(Organisation).order_by(Organisation.created_at.asc())
    )

    if organisation is None:
        organisation = Organisation(name="BrandShield Demo Organisation")
        db.add(organisation)
        db.commit()
        db.refresh(organisation)

    return organisation


@router.post(
    "",
    response_model=BrandGuidelineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_guideline(
    payload: BrandGuidelineCreate,
    db: Session = Depends(get_db),
):
    organisation = get_default_organisation(db)

    guideline = BrandGuideline(
        organisation_id=organisation.id,
        title=payload.title,
        category=payload.category,
        rule=payload.rule,
    )

    db.add(guideline)
    db.commit()
    db.refresh(guideline)

    return guideline


@router.get("", response_model=list[BrandGuidelineResponse])
def list_guidelines(
    active_only: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    organisation = get_default_organisation(db)

    statement = select(BrandGuideline).where(
        BrandGuideline.organisation_id == organisation.id
    )

    if active_only:
        statement = statement.where(BrandGuideline.is_active.is_(True))

    statement = statement.order_by(BrandGuideline.created_at.desc())

    return list(db.scalars(statement).all())


@router.get("/{guideline_id}", response_model=BrandGuidelineResponse)
def get_guideline(
    guideline_id: UUID,
    db: Session = Depends(get_db),
):
    organisation = get_default_organisation(db)

    guideline = db.scalar(
        select(BrandGuideline).where(
            BrandGuideline.id == guideline_id,
            BrandGuideline.organisation_id == organisation.id,
        )
    )

    if guideline is None:
        raise HTTPException(
            status_code=404,
            detail="Brand guideline not found",
        )

    return guideline


@router.put("/{guideline_id}", response_model=BrandGuidelineResponse)
def update_guideline(
    guideline_id: UUID,
    payload: BrandGuidelineUpdate,
    db: Session = Depends(get_db),
):
    organisation = get_default_organisation(db)

    guideline = db.scalar(
        select(BrandGuideline).where(
            BrandGuideline.id == guideline_id,
            BrandGuideline.organisation_id == organisation.id,
        )
    )

    if guideline is None:
        raise HTTPException(
            status_code=404,
            detail="Brand guideline not found",
        )

    changes = payload.model_dump(exclude_unset=True)

    for field, value in changes.items():
        setattr(guideline, field, value)

    db.commit()
    db.refresh(guideline)

    return guideline


@router.delete("/{guideline_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guideline(
    guideline_id: UUID,
    db: Session = Depends(get_db),
):
    organisation = get_default_organisation(db)

    guideline = db.scalar(
        select(BrandGuideline).where(
            BrandGuideline.id == guideline_id,
            BrandGuideline.organisation_id == organisation.id,
        )
    )

    if guideline is None:
        raise HTTPException(
            status_code=404,
            detail="Brand guideline not found",
        )

    db.delete(guideline)
    db.commit()

    return None
