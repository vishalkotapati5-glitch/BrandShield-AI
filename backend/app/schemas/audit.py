
from pydantic import BaseModel, Field


class AuditRequest(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=10000,
        description="Content to check against brand guidelines",
    )


class AuditFinding(BaseModel):
    guideline: str
    severity: str
    problem: str
    suggestion: str
    quoted_text: str


class AuditResponse(BaseModel):
    overall_status: str
    summary: str
    findings: list[AuditFinding]
