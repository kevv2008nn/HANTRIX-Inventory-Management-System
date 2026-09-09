from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SimulationAction(str, Enum):
    PERSON_DETECTED = "PERSON_DETECTED"
    AUTHENTICATE = "AUTHENTICATE"
    ENTRY = "ENTRY"
    TAKE = "TAKE"
    VERIFY_MATCH = "VERIFY_MATCH"
    VERIFY_MISMATCH = "VERIFY_MISMATCH"
    EXIT = "EXIT"


class SimulationStartRequest(BaseModel):
    student_id: str = Field(..., min_length=1)
    authentication_method: str = "FACE"
    camera_id: str = "camera_1"


class SimulationComponentRequest(BaseModel):
    student_id: str = Field(..., min_length=1)
    component_id: str = Field(..., min_length=1)
    quantity: int = Field(default=1, ge=1)
    camera_id: str = "camera_2"


class SimulationVerificationRequest(BaseModel):
    transaction_id: str
    expected_component: str
    detected_component: str = ""
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    camera_id: str = "camera_2"


class SimulationExitRequest(BaseModel):
    student_id: str = Field(..., min_length=1)


class SimulationResult(BaseModel):
    success: bool
    action: str
    message: str

    student_id: Optional[str] = None
    attendance_id: Optional[str] = None
    session_id: Optional[str] = None
    lab_session_id: Optional[str] = None
    transaction_id: Optional[str] = None

    verification_status: Optional[str] = None
    transaction_status: Optional[str] = None

    camera_id: Optional[str] = None
    component_id: Optional[str] = None
    quantity: Optional[int] = None
    confidence: Optional[float] = None

    inventory_updated: bool = False
    alert_created: bool = False

    stage: Optional[str] = None


class FullSimulationRequest(BaseModel):
    student_id: str = Field(..., min_length=1)
    component_id: str = Field(..., min_length=1)
    quantity: int = Field(default=1, ge=1)

    authentication_method: str = "FACE"

    camera_1: str = "camera_1"
    camera_2: str = "camera_2"

    verification_mode: str = "MATCH"

    confidence: float = Field(
        default=0.95,
        ge=0.0,
        le=1.0,
    )


class FullSimulationResponse(BaseModel):
    success: bool
    message: str

    student_id: str

    attendance_id: Optional[str] = None
    session_id: Optional[str] = None
    lab_session_id: Optional[str] = None
    transaction_id: Optional[str] = None

    verification_status: Optional[str] = None

    inventory_updated: bool = False
    alert_created: bool = False

    steps: list[SimulationResult] = Field(default_factory=list)