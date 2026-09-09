from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.events.schemas import (
    EventResult,
    SmartLabEvent,
)

from app.events.service import (
    process_event,
    simulate_component_mismatch,
    simulate_person_detected,
    simulate_system_warning,
    simulate_unknown_person,
)


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


# ============================================================
# PROCESS REAL EVENT
# ============================================================

@router.post(
    "/",
    response_model=EventResult,
)
def process_event_endpoint(
    event: SmartLabEvent,
    db: Session = Depends(get_db),
):
    return process_event(
        db=db,
        event=event,
    )


# ============================================================
# TEST: PERSON DETECTED
# ============================================================

@router.post(
    "/test/person",
    response_model=EventResult,
)
def test_person_event(
    db: Session = Depends(get_db),
):

    return simulate_person_detected(
        db=db,
        camera_id="camera_1",
        confidence=0.95,
    )


# ============================================================
# TEST: UNKNOWN PERSON
# ============================================================

@router.post(
    "/test/unknown",
    response_model=EventResult,
)
def test_unknown_event(
    db: Session = Depends(get_db),
):

    return simulate_unknown_person(
        db=db,
        camera_id="camera_1",
        confidence=0.87,
    )


# ============================================================
# TEST: COMPONENT MISMATCH
# ============================================================

@router.post(
    "/test/mismatch",
    response_model=EventResult,
)
def test_mismatch_event(
    db: Session = Depends(get_db),
):

    # IMPORTANT:
    #
    # Do NOT use:
    #
    # student_id="TEST-STUDENT"
    #
    # because TEST-STUDENT does not exist in the
    # students table and alerts.student_id has
    # a foreign-key constraint.
    #
    # For a pure mismatch simulation we use NULL.

    return simulate_component_mismatch(
        db=db,
        camera_id="camera_2",
        component_id="ESP32-001",
        expected_component="ESP32",
        detected_component="Arduino UNO",
        student_id=None,
        confidence=0.94,
        transaction_id=None,
    )


# ============================================================
# TEST: SYSTEM WARNING
# ============================================================

@router.post(
    "/test/system-warning",
    response_model=EventResult,
)
def test_system_warning_event(
    db: Session = Depends(get_db),
):

    return simulate_system_warning(
        db=db,
        title="AI Engine Warning",
        message=(
            "The simulated AI engine reported "
            "a warning."
        ),
        severity="WARNING",
        camera_id=None,
    )