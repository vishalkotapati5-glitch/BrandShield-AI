
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BrandGuidelineCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    category: str = Field(min_length=2, max_length=50)
    rule: str = Field(min_length=3)


class BrandGuidelineUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    category: str | None = Field(default=None, min_length=2, max_length=50)
    rule: str | None = Field(default=None, min_length=3)
    is_active: bool | None = None


class BrandGuidelineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organisation_id: UUID
    title: str
    category: str
    rule: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
