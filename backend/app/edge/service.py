from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.edge.schemas import (
    EdgeHeartbeatRequest,
    CameraHeartbeatRequest,
    DetectionRequest,
    EdgeEventRequest,
    EdgeVerificationRequest,
)


# ============================================================
# RUNTIME EDGE STATE
# ============================================================

edge_devices: dict[str, dict[str, Any]] = {}

camera_devices: dict[str, dict[str, Any]] = {}


# ============================================================
# TIME
# ============================================================

def utc_now() -> datetime:

    return datetime.now(timezone.utc)


# ============================================================
# EDGE HEARTBEAT
# ============================================================

def process_edge_heartbeat(
    request: EdgeHeartbeatRequest,
):

    now = utc_now()

    edge_devices[request.device_id] = {

        "device_id": request.device_id,

        "device_name": request.device_name,

        "ip_address": request.ip_address,

        "hostname": request.hostname,

        "cpu_usage": request.cpu_usage,

        "memory_usage": request.memory_usage,

        "temperature": request.temperature,

        "ai_status": request.ai_status,

        "cameras_status": request.cameras_status,

        "status": "ONLINE",

        "last_seen": now,

        "metadata": request.metadata,
    }

    return {

        "success": True,

        "message": "Edge heartbeat received.",

        "device_id": request.device_id,

        "status": "ONLINE",

        "last_seen": now,

    }


# ============================================================
# CAMERA HEARTBEAT
# ============================================================

def process_camera_heartbeat(
    request: CameraHeartbeatRequest,
):

    now = utc_now()

    camera_devices[request.camera_id] = {

        "device_id": request.device_id,

        "camera_id": request.camera_id,

        "status": request.status,

        "fps": request.fps,

        "resolution": request.resolution,

        "ai_status": request.ai_status,

        "last_seen": now,

        "metadata": request.metadata,
    }

    return {

        "success": True,

        "message": "Camera heartbeat received.",

        "device_id": request.device_id,

        "camera_id": request.camera_id,

        "status": request.status,

        "last_seen": now,

    }


# ============================================================
# DETECTION
# ============================================================

def process_detection(
    request: DetectionRequest,
):

    now = request.timestamp or utc_now()

    return {

        "success": True,

        "message": "AI detection received.",

        "device_id": request.device_id,

        "camera_id": request.camera_id,

        "detection_type": request.detection_type,

        "label": request.label,

        "confidence": request.confidence,

        "timestamp": now,

        "bbox": request.bbox,

        "metadata": request.metadata,
    }


# ============================================================
# EVENT
# ============================================================

def process_edge_event(
    db: Session,
    request: EdgeEventRequest,
):

    from app.events.schemas import SmartLabEvent
    from app.events.service import process_event

    event = SmartLabEvent(

        event_type=request.event_type,

        student_id=request.student_id,

        component_id=request.component_id,

        camera_id=request.camera_id,

        confidence=request.confidence,

        metadata=request.metadata,
    )

    result = process_event(
        db=db,
        event=event,
    )

    return {

        "success": True,

        "message": "Edge event processed.",

        "device_id": request.device_id,

        "camera_id": request.camera_id,

        "event_type": request.event_type,

        "result": result,

    }


# ============================================================
# CAMERA 2 VERIFICATION
# ============================================================

def process_verification(
    db: Session,
    request: EdgeVerificationRequest,
):

    from app.transactions.service import (
        verify_transaction,
        get_transaction,
    )

    import uuid

    try:

        transaction_id = uuid.UUID(
            str(request.transaction_id)
        )

    except ValueError:

        return {

            "success": False,

            "message": "Invalid transaction_id.",

            "device_id": request.device_id,

            "camera_id": request.camera_id,

        }

    transaction = get_transaction(
        db=db,
        transaction_id=transaction_id,
    )

    if transaction is None:

        return {

            "success": False,

            "message": "Transaction not found.",

            "device_id": request.device_id,

            "camera_id": request.camera_id,

        }

    verified = verify_transaction(

        db=db,

        transaction_id=transaction_id,

        detected_component=request.detected_component,

        camera_id=request.camera_id,

        confidence=request.confidence,
    )

    matched = (

        verified.verification_status
        == "MATCHED"

    )

    approved = (

        verified.status
        in ["APPROVED", "COMPLETED"]

    )

    return {

        "success": matched and approved,

        "message": (

            "Camera 2 verification matched."
            if matched and approved
            else
            "Camera 2 verification failed."
        ),

        "device_id": request.device_id,

        "camera_id": request.camera_id,

        "transaction_id": str(
            verified.transaction_id
        ),

        "expected_component":
            request.expected_component,

        "detected_component":
            request.detected_component,

        "confidence":
            request.confidence,

        "verification_status":
            verified.verification_status,

        "transaction_status":
            verified.status,

        "inventory_updated":
            matched and approved,

    }


# ============================================================
# EDGE STATUS
# ============================================================

def get_edge_status():

    return {

        "status": "ONLINE",

        "timestamp": utc_now(),

        "devices": list(
            edge_devices.values()
        ),

        "cameras": list(
            camera_devices.values()
        ),

    }