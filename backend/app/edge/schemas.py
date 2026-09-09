from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# ============================================================
# EDGE HEARTBEAT
# ============================================================

class EdgeHeartbeatRequest(BaseModel):

    device_id: str
    device_name: str = "Raspberry Pi"
    ip_address: Optional[str] = None
    hostname: Optional[str] = None

    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    temperature: Optional[float] = None

    ai_status: str = "ONLINE"
    cameras_status: str = "UNKNOWN"

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# CAMERA HEARTBEAT
# ============================================================

class CameraHeartbeatRequest(BaseModel):

    device_id: str
    camera_id: str

    status: str = "ONLINE"

    fps: Optional[float] = None
    resolution: Optional[str] = None

    ai_status: str = "ONLINE"

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# AI DETECTION
# ============================================================

class DetectionRequest(BaseModel):

    device_id: str
    camera_id: str

    detection_type: str
    label: str

    confidence: Optional[float] = None

    timestamp: Optional[datetime] = None

    bbox: Optional[list[float]] = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# EDGE EVENT
# ============================================================

class EdgeEventRequest(BaseModel):

    device_id: str
    camera_id: Optional[str] = None

    event_type: str

    student_id: Optional[str] = None
    component_id: Optional[str] = None

    confidence: Optional[float] = None

    timestamp: Optional[datetime] = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# CAMERA 2 VERIFICATION
# ============================================================

class EdgeVerificationRequest(BaseModel):

    device_id: str
    camera_id: str = "camera_2"

    transaction_id: str

    expected_component: str
    detected_component: str

    confidence: Optional[float] = None

    timestamp: Optional[datetime] = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# RESPONSE
# ============================================================

class EdgeResponse(BaseModel):

    success: bool
    message: str

    device_id: Optional[str] = None
    camera_id: Optional[str] = None

    event_type: Optional[str] = None

    timestamp: datetime

    data: dict[str, Any] = Field(
        default_factory=dict
    )