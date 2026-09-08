from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AlertCreate(BaseModel):
    alert_type: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)

    severity: str = Field(
        default="INFO",
        max_length=30
    )

    student_id: Optional[str] = None
    component_id: Optional[str] = None
    camera_id: Optional[str] = None
    transaction_id: Optional[UUID] = None

    metadata: Optional[dict[str, Any]] = None


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    alert_id: UUID
    alert_type: str
    title: str
    message: str
    severity: str

    student_id: Optional[str] = None
    component_id: Optional[str] = None
    camera_id: Optional[str] = None
    transaction_id: Optional[UUID] = None

    status: str

    metadata: Optional[dict[str, Any]] = None

    created_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class AlertResolve(BaseModel):
    status: str = Field(
        default="RESOLVED",
        max_length=30
    )