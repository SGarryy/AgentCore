"""Request/response schemas with validation."""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from app.constants import Priority, Status


class TaskRequest(BaseModel):
    """User task request."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        example="Onboard new developer John",
    )
    priority: Optional[Priority] = Field(default=Priority.MEDIUM, description="Task priority level")

    @field_validator("text")
    @classmethod
    def text_not_whitespace(cls, v):
        """Ensure text is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError("Task text cannot be empty or whitespace only")
        return v.strip()


class ExtractedEntities(BaseModel):
    """Extracted named entities from text."""

    persons: List[str] = Field(default_factory=list, example=["John", "Alice"])
    dates: List[str] = Field(default_factory=list, example=["2026-05-20"])
    orgs: List[str] = Field(default_factory=list, example=["Engineering"])
    misc: List[str] = Field(default_factory=list)


class IntentResult(BaseModel):
    """Result of intent extraction."""

    raw_text: str
    intent: str
    entities: ExtractedEntities
    priority: str
    matched_keywords: List[str]
    timestamp: str


class AgentResult(BaseModel):
    """Agent execution result."""

    agent: str = Field(..., example="HR Onboarding Agent")
    status: str = Field(..., example="success")
    steps: List[str] = Field(..., example=["Created profile", "Sent email"])
    output: str = Field(..., example="Onboarding completed")
    timestamp: str = Field(..., example="2026-05-12T10:30:00Z")


class ErrorResponse(BaseModel):
    """Standardized error response."""

    error: str = Field(..., example="Invalid input")
    error_code: str = Field(..., example="VALIDATION_ERROR")
    details: Optional[dict] = Field(default=None)
    timestamp: str = Field(..., example="2026-05-12T10:30:00Z")
    request_id: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., example="healthy", description="Overall health status")
    timestamp: str = Field(..., example="2026-05-12T10:30:00Z")
    checks: Optional[dict] = Field(
        default=None,
        example={"ollama": {"status": "healthy"}, "model": {"status": "healthy"}},
    )


class RouterResult(BaseModel):
    """ML Router result."""

    routed_to: str = Field(..., example="hr_agent")
    confidence: float = Field(..., ge=0.0, le=1.0, example=0.95)
    all_scores: dict = Field(..., example={"hr_agent": 0.95, "finance_agent": 0.03})
