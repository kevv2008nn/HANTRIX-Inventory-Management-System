from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# =========================================================
# TRANSACTION CREATE
# =========================================================

class TransactionCreate(BaseModel):

    student_id: str

    component_id: str

    action: str

    quantity: int = Field(
        default=1,
        gt=0,
    )


# =========================================================
# TAKE REQUEST
# =========================================================

class TakeRequest(BaseModel):

    student_id: str

    component_id: str

    quantity: int = Field(
        default=1,
        gt=0,
    )


# =========================================================
# RETURN REQUEST
# =========================================================

class ReturnRequest(BaseModel):

    student_id: str

    component_id: str

    quantity: int = Field(
        default=1,
        gt=0,
    )


# =========================================================
# CAMERA-2 VERIFICATION REQUEST
# =========================================================

class VerificationRequest(BaseModel):

    detected_component: str = Field(
        ...,
        min_length=1,
    )

    confidence: float = Field(
        ge=0,
        le=1,
    )

    camera_id: Optional[str] = None


# =========================================================
# TRANSACTION RESPONSE
# =========================================================

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