from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.authentication.schemas import (
    PersonDetectedRequest,
    FaceRecognitionRequest,
    QRScanRequest,
    LabActionRequest,
    AuthenticationResult,
    AuthenticationActionResult,
)

from app.authentication.service import authentication_service


router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"],
)


# =========================================================
# PERSON DETECTED
# =========================================================

@router.post(
    "/person",
    response_model=AuthenticationResult,
)
def person_detected(
    data: PersonDetectedRequest,
):

    return authentication_service.person_detected(
        camera_id=data.camera_id,
        confidence=data.confidence,
    )


# =========================================================
# FACE
# =========================================================

@router.post(
    "/{session_id}/face",
    response_model=AuthenticationResult,
)
def face_recognition(
    session_id: str,
    data: FaceRecognitionRequest,
    db: Session = Depends(get_db),
):

    return authentication_service.face_recognized(
        session_id=session_id,
        student_id=data.student_id,
        confidence=data.confidence,
        recognized=data.recognized,
        db=db,
    )


# =========================================================
# QR
# =========================================================

@router.post(
    "/{session_id}/qr",
    response_model=AuthenticationResult,
)
def qr_authentication(
    session_id: str,
    data: QRScanRequest,
    db: Session = Depends(get_db),
):

    return authentication_service.qr_scanned(
        session_id=session_id,
        student_id=data.student_id,
        valid=data.valid,
        db=db,
    )


# =========================================================
# EXPLICIT ENTRY / EXIT
# =========================================================

@router.post(
    "/{session_id}/action",
    response_model=AuthenticationActionResult,
)
def lab_action(
    session_id: str,
    data: LabActionRequest,
    db: Session = Depends(get_db),
):

    return authentication_service.perform_lab_action(
        session_id=session_id,
        action=data.action,
        db=db,
    )


# =========================================================
# GET SESSION
# =========================================================

@router.get(
    "/{session_id}",
)
def get_authentication_session(
    session_id: str,
):

    session = authentication_service.get_session(
        session_id
    )

    if session is None:

        return {
            "found": False,
            "message": "Authentication session not found.",
        }

    return session


# =========================================================
# RESET
# =========================================================

@router.post(
    "/{session_id}/reset",
    response_model=AuthenticationResult,
)
def reset_authentication_session(
    session_id: str,
):

    return authentication_service.reset_session(
        session_id
    )


# =========================================================
# ACTIVE
# =========================================================

@router.get(
    "/runtime/active",
)
def active_authentication_sessions():

    return authentication_service.get_active_sessions()


# =========================================================
# AUTHENTICATED
# =========================================================

@router.get(
    "/runtime/authenticated",
)
def authenticated_sessions():

    return authentication_service.get_authenticated_sessions()