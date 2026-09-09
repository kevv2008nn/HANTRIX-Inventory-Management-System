from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.simulation.schemas import (
    FullSimulationRequest,
    FullSimulationResponse,
    SimulationComponentRequest,
    SimulationExitRequest,
    SimulationResult,
    SimulationStartRequest,
    SimulationVerificationRequest,
)

from app.simulation.service import (
    get_simulation_status,
    simulate_authentication,
    simulate_entry,
    simulate_exit,
    simulate_full_flow,
    simulate_match,
    simulate_mismatch,
    simulate_person_detection,
    simulate_take,
)


router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"],
)


# ============================================================
# STATUS
# ============================================================

@router.get("/status")
def simulation_status(
    db: Session = Depends(get_db),
):
    return get_simulation_status(db)


# ============================================================
# PERSON DETECTION
# ============================================================

@router.post(
    "/person",
    response_model=SimulationResult,
)
def simulation_person(
    db: Session = Depends(get_db),
):

    return simulate_person_detection(
        db=db,
        camera_id="camera_1",
        confidence=0.95,
    )


# ============================================================
# AUTHENTICATION
# ============================================================

@router.post(
    "/authenticate",
    response_model=SimulationResult,
)
def simulation_authenticate(
    request: SimulationStartRequest,
    db: Session = Depends(get_db),
):

    return simulate_authentication(
        db=db,
        student_id=request.student_id,
        authentication_method=(
            request.authentication_method
        ),
        camera_id=request.camera_id,
    )


# ============================================================
# ENTRY
# ============================================================

@router.post(
    "/entry",
    response_model=SimulationResult,
)
def simulation_entry(
    request: SimulationStartRequest,
    db: Session = Depends(get_db),
):

    authentication = simulate_authentication(
        db=db,
        student_id=request.student_id,
        authentication_method=(
            request.authentication_method
        ),
        camera_id=request.camera_id,
    )

    if not authentication["success"]:

        return authentication

    return simulate_entry(
        db=db,
        authentication_session_id=(
            authentication["session_id"]
        ),
        student_id=request.student_id,
    )


# ============================================================
# TAKE COMPONENT
# ============================================================

@router.post(
    "/take",
    response_model=SimulationResult,
)
def simulation_take(
    request: SimulationComponentRequest,
    db: Session = Depends(get_db),
):

    return simulate_take(
        db=db,
        student_id=request.student_id,
        component_id=request.component_id,
        quantity=request.quantity,
    )


# ============================================================
# CAMERA 2 MATCH
# ============================================================

@router.post(
    "/verify-match",
    response_model=SimulationResult,
)
def simulation_verify_match(
    request: SimulationVerificationRequest,
    db: Session = Depends(get_db),
):

    return simulate_match(
        db=db,
        transaction_id=request.transaction_id,
        expected_component=(
            request.expected_component
        ),
        confidence=request.confidence,
        camera_id=request.camera_id,
    )


# ============================================================
# CAMERA 2 MISMATCH
# ============================================================

@router.post(
    "/verify-mismatch",
    response_model=SimulationResult,
)
def simulation_verify_mismatch(
    request: SimulationVerificationRequest,
    db: Session = Depends(get_db),
):

    return simulate_mismatch(
        db=db,
        transaction_id=request.transaction_id,
        expected_component=(
            request.expected_component
        ),
        detected_component=(
            request.detected_component
        ),
        confidence=request.confidence,
        camera_id=request.camera_id,
    )


# ============================================================
# EXPLICIT EXIT
# ============================================================

@router.post(
    "/exit",
    response_model=SimulationResult,
)
def simulation_exit(
    request: SimulationExitRequest,
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # EXIT STATION AUTHENTICATION
    #
    # The student authenticates AGAIN at the EXIT station.
    #
    # This creates a fresh authentication runtime session.
    # It does NOT create a new attendance or lab session.
    # --------------------------------------------------------

    authentication = simulate_authentication(
        db=db,
        student_id=request.student_id,
        authentication_method="FACE",
        camera_id="camera_1",
    )

    if not authentication["success"]:

        return SimulationResult(
            success=False,
            action="EXIT",
            message=(
                "Exit authentication failed."
            ),
            student_id=request.student_id,
            session_id=authentication.get(
                "session_id"
            ),
        )

    # --------------------------------------------------------
    # CLOSE EXISTING DATABASE SESSION
    # --------------------------------------------------------

    return simulate_exit(
        db=db,
        authentication_session_id=(
            authentication["session_id"]
        ),
        student_id=request.student_id,
    )


# ============================================================
# FULL FLOW
# ============================================================

@router.post(
    "/full-flow",
    response_model=FullSimulationResponse,
)
def simulation_full_flow(
    request: FullSimulationRequest,
    db: Session = Depends(get_db),
):

    return simulate_full_flow(
        db=db,
        student_id=request.student_id,
        component_id=request.component_id,
        quantity=request.quantity,
        authentication_method=(
            request.authentication_method
        ),
        camera_1=request.camera_1,
        camera_2=request.camera_2,
        verification_mode=(
            request.verification_mode
        ),
        confidence=request.confidence,
    )