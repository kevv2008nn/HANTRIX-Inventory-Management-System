from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.edge.schemas import (
    EdgeHeartbeatRequest,
    CameraHeartbeatRequest,
    DetectionRequest,
    EdgeEventRequest,
    EdgeVerificationRequest,
)

from app.edge.service import (
    process_edge_heartbeat,
    process_camera_heartbeat,
    process_detection,
    process_edge_event,
    process_verification,
    get_edge_status,
)


router = APIRouter(
    prefix="/edge",
    tags=["Edge Gateway"],
)


# ============================================================
# EDGE STATUS
# ============================================================

@router.get("/status")
def edge_status():

    return get_edge_status()


# ============================================================
# RASPBERRY PI HEARTBEAT
# ============================================================

@router.post("/heartbeat")
def edge_heartbeat(
    request: EdgeHeartbeatRequest,
):

    return process_edge_heartbeat(
        request
    )


# ============================================================
# CAMERA HEARTBEAT
# ============================================================

@router.post("/camera/heartbeat")
def camera_heartbeat(
    request: CameraHeartbeatRequest,
):

    return process_camera_heartbeat(
        request
    )


# ============================================================
# AI DETECTION
# ============================================================

@router.post("/detections")
def edge_detection(
    request: DetectionRequest,
):

    return process_detection(
        request
    )


# ============================================================
# EDGE EVENT
# ============================================================

@router.post("/events")
def edge_event(
    request: EdgeEventRequest,
    db: Session = Depends(get_db),
):

    return process_edge_event(
        db=db,
        request=request,
    )


# ============================================================
# CAMERA 2 VERIFICATION
# ============================================================

@router.post("/verification")
def edge_verification(
    request: EdgeVerificationRequest,
    db: Session = Depends(get_db),
):

    return process_verification(
        db=db,
        request=request,
    )