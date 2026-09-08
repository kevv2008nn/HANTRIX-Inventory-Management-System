from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):

    student_id: str

    component_id: str

    action: str

    quantity: int = Field(
        default=1,
        gt=0,
    )


class TakeRequest(BaseModel):

    student_id: str

    component_id: str

    quantity: int = Field(
        default=1,
        gt=0,
    )


class ReturnRequest(BaseModel):

    student_id: str

    component_id: str

    quantity: int = Field(
        default=1,
        gt=0,
    )


class VerificationRequest(BaseModel):

    detected_label: str

    confidence: float = Field(
        ge=0,
        le=1,
    )

    camera_id: Optional[str] = None


class TransactionResponse(BaseModel):

    transaction_id: UUID

    student_id: str

    component_id: str

    action: str

    quantity: int

    requested_at: datetime

    borrowed_at: Optional[datetime] = None

    returned_at: Optional[datetime] = None

    status: str

    verification_status: str

    expected_rack: Optional[str] = None

    expected_shelf: Optional[str] = None

    camera_id: Optional[str] = None

    confidence: Optional[float] = None

    mismatch_reason: Optional[str] = None

    created_at: datetime

    updated_at: datetime