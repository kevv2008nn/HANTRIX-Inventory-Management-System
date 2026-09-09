from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# EVENT TYPES
# ============================================================

EVENT_TYPES = {
    "PERSON_DETECTED",
    "FACE_RECOGNIZED",
    "QR_SCANNED",
    "PERSON_ENTERED",
    "PERSON_EXITED",

    "ATTENDANCE_MARKED",
    "SESSION_STARTED",
    "SESSION_ENDED",

    "TRANSACTION_CREATED",
    "TRANSACTION_VERIFIED",
    "TRANSACTION_APPROVED",
    "TRANSACTION_REJECTED",

    "COMPONENT_DETECTED",
    "COMPONENT_PICKED",
    "COMPONENT_RETURNED",
    "COMPONENT_MISMATCH",

    "LOW_STOCK",
    "UNKNOWN_PERSON",
    "OVERDUE",

    "CAMERA_ONLINE",
    "CAMERA_OFFLINE",

    "SYSTEM_WARNING",
    "SYSTEM_ERROR",
}


# ============================================================
# EVENT SEVERITIES
# ============================================================

EVENT_SEVERITIES = {
    "INFO",
    "WARNING",
    "HIGH",
    "CRITICAL",
}


# ============================================================
# SMARTLAB EVENT
# ============================================================

class SmartLabEvent(BaseModel):
    """
    Standard event format used by SmartLab subsystems.

    Raspberry Pi edge AI, cameras, QR, face recognition,
    transactions, inventory and system services can all
    communicate with the backend using this structure.
    """

    model_config = ConfigDict(
        extra="allow"
    )

    event_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    source: str = Field(
        default="SYSTEM",
        max_length=100,
    )

    camera_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    student_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    component_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    transaction_id: Optional[str] = None

    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    severity: str = Field(
        default="INFO",
        max_length=30,
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    data: dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# EVENT RESULT
# ============================================================

class EventResult(BaseModel):
    """
    Result returned by the SmartLab Event Engine.

    session_id and authentication_state are populated
    when a PERSON_DETECTED event starts authentication.
    """

    accepted: bool

    event_type: str

    message: str

    # --------------------------------------------------------
    # AUTHENTICATION CONTEXT
    # --------------------------------------------------------

    session_id: Optional[str] = None

    authentication_state: Optional[str] = None

    authenticated: bool = False

    student_id: Optional[str] = None

    # --------------------------------------------------------
    # ALERT CONTEXT
    # --------------------------------------------------------

    alert_created: bool = False

    alert_id: Optional[str] = None

    # --------------------------------------------------------
    # PROCESSING TIME
    # --------------------------------------------------------

    processed_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )