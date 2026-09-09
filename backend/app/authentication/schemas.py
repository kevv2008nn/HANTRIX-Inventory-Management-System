from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AuthenticationState(str, Enum):
    IDLE = "IDLE"
    PERSON_DETECTED = "PERSON_DETECTED"
    AUTHENTICATING = "AUTHENTICATING"
    FACE_RECOGNIZED = "FACE_RECOGNIZED"
    QR_SCANNED = "QR_SCANNED"
    AUTHENTICATED = "AUTHENTICATED"
    UNKNOWN = "UNKNOWN"
    REJECTED = "REJECTED"


class AuthenticationMethod(str, Enum):
    FACE = "FACE"
    QR = "QR"
    NONE = "NONE"


class LabAction(str, Enum):
    ENTRY = "ENTRY"
    EXIT = "EXIT"


class AuthenticationSession(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    session_id: str
    camera_id: Optional[str] = None
    student_id: Optional[str] = None

    state: AuthenticationState = AuthenticationState.IDLE
    method: AuthenticationMethod = AuthenticationMethod.NONE

    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    authenticated: bool = False
    unknown: bool = False

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class PersonDetectedRequest(BaseModel):
    camera_id: str = Field(..., min_length=1, max_length=100)

    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )


class FaceRecognitionRequest(BaseModel):
    camera_id: str = Field(..., min_length=1, max_length=100)

    student_id: Optional[str] = None

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    recognized: bool = True


class QRScanRequest(BaseModel):
    camera_id: str = Field(..., min_length=1, max_length=100)

    student_id: Optional[str] = None

    valid: bool = True


class LabActionRequest(BaseModel):
    action: LabAction


class AuthenticationResult(BaseModel):
    accepted: bool

    state: AuthenticationState

    authenticated: bool

    unknown: bool

    student_id: Optional[str] = None

    method: AuthenticationMethod = AuthenticationMethod.NONE

    confidence: Optional[float] = None

    message: str

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class AuthenticationActionResult(BaseModel):
    accepted: bool
    student_id: str
    action: LabAction
    attendance_id: Optional[str] = None
    lab_session_id: Optional[str] = None
    message: str