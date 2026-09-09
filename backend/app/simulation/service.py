import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.authentication.schemas import AuthenticationMethod
from app.authentication.service import authentication_service

from app.attendance.models import Attendance
from app.attendance.service import (
    check_in,
    check_out,
)

from app.lab_sessions.models import LabSession
from app.lab_sessions.service import (
    start_session,
    end_session,
)

from app.transactions.service import (
    create_take_transaction,
    verify_transaction,
    get_transaction,
)

from app.models.inventory import Inventory

from app.events.service import (
    simulate_component_mismatch,
)


# ============================================================
# RUNTIME STATE
# ============================================================

# Runtime information only.
#
# IMPORTANT:
# Database attendance/lab-session/transaction state is the
# source of truth. This dictionary is only supplementary.
#
simulation_sessions: dict[str, dict[str, Any]] = {}


# ============================================================
# HELPERS
# ============================================================

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _result(
    success: bool,
    message: str,
    action: str = "UNKNOWN",
    **kwargs,
) -> dict[str, Any]:

    result = {
        "success": success,
        "action": action,
        "message": message,
    }

    result.update(kwargs)

    return result


def _serialize(value):

    if value is None:
        return None

    if isinstance(value, uuid.UUID):
        return str(value)

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, dict):
        return {
            str(key): _serialize(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _serialize(item)
            for item in value
        ]

    if hasattr(value, "model_dump"):
        return _serialize(
            value.model_dump()
        )

    if hasattr(value, "__table__"):

        data = {}

        for column in value.__table__.columns:

            data[column.name] = _serialize(
                getattr(
                    value,
                    column.name,
                )
            )

        return data

    return value


def _authentication_method(
    method: str | AuthenticationMethod,
) -> AuthenticationMethod:

    if isinstance(
        method,
        AuthenticationMethod,
    ):
        return method

    try:

        return AuthenticationMethod(
            str(method).upper()
        )

    except ValueError:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid authentication_method. "
                "Use FACE or QR."
            ),
        )


def _find_authenticated_session(
    student_id: str,
):

    sessions = (
        authentication_service
        .get_authenticated_sessions()
    )

    matching = [
        session
        for session in sessions
        if str(session.student_id)
        == str(student_id)
    ]

    if not matching:
        return None

    return max(
        matching,
        key=lambda session: (
            session.updated_at
            or datetime.min.replace(
                tzinfo=timezone.utc
            )
        ),
    )


def _get_or_create_simulation_session(
    authentication_session_id: str,
    student_id: str,
    camera_id: str = "camera_1",
    authentication_method: str = "FACE",
):

    if authentication_session_id not in simulation_sessions:

        simulation_sessions[
            authentication_session_id
        ] = {
            "student_id": str(student_id),
            "camera_id": camera_id,
            "authentication_method": (
                authentication_method
            ),
            "authenticated_at": utc_now(),
            "entry": None,
            "attendance_id": None,
            "lab_session_id": None,
            "transactions": [],
            "exit": None,
            "completed": False,
        }

    return simulation_sessions[
        authentication_session_id
    ]


# ============================================================
# DATABASE ACTIVE ATTENDANCE
# ============================================================

def _get_active_attendance(
    student_id: str,
    db: Session,
) -> Optional[Attendance]:

    return (
        db.query(Attendance)
        .filter(
            Attendance.student_id == str(student_id),
            Attendance.exit_time.is_(None),
            Attendance.status == "IN",
        )
        .order_by(
            Attendance.entry_time.desc()
        )
        .first()
    )


# ============================================================
# DATABASE ACTIVE LAB SESSION
# ============================================================

def _get_active_lab_session(
    student_id: str,
    db: Session,
) -> Optional[LabSession]:

    return (
        db.query(LabSession)
        .filter(
            LabSession.student_id == str(student_id),
            LabSession.status == "ACTIVE",
            LabSession.end_time.is_(None),
        )
        .order_by(
            LabSession.start_time.desc()
        )
        .first()
    )


# ============================================================
# SIMULATION STATUS
# ============================================================

def get_simulation_status(
    db: Session,
):

    inventory_count = (
        db.query(Inventory)
        .count()
    )

    authenticated_sessions = (
        authentication_service
        .get_authenticated_sessions()
    )

    active_db_sessions = (
        db.query(LabSession)
        .filter(
            LabSession.status == "ACTIVE",
            LabSession.end_time.is_(None),
        )
        .count()
    )

    return {
        "simulation": "READY",
        "backend": "ONLINE",
        "inventory_items": inventory_count,
        "authenticated_sessions": len(
            authenticated_sessions
        ),
        "active_simulation_sessions": len(
            [
                session
                for session in simulation_sessions.values()
                if not session.get("completed", False)
            ]
        ),
        "active_database_lab_sessions": (
            active_db_sessions
        ),
        "timestamp": utc_now().isoformat(),
    }


# ============================================================
# PERSON DETECTION
# ============================================================

def simulate_person_detection(
    db: Session,
    camera_id: str = "camera_1",
    confidence: float = 0.95,
):

    result = authentication_service.person_detected(
        camera_id=camera_id,
        confidence=confidence,
    )

    active_sessions = (
        authentication_service
        .get_active_sessions()
    )

    session_id = None

    if active_sessions:

        latest = max(
            active_sessions,
            key=lambda session: (
                session.updated_at
                or datetime.min.replace(
                    tzinfo=timezone.utc
                )
            ),
        )

        session_id = latest.session_id

    return _result(
        success=result.accepted,
        action="PERSON_DETECTED",
        message=result.message,
        stage="PERSON_DETECTED",
        camera_id=camera_id,
        confidence=confidence,
        authentication=_serialize(result),
        session_id=session_id,
    )


# ============================================================
# AUTHENTICATION
# ============================================================

def simulate_authentication(
    db: Session,
    student_id: str,
    authentication_method: str,
    camera_id: str = "camera_1",
):

    method = _authentication_method(
        authentication_method
    )

    person_result = (
        authentication_service.person_detected(
            camera_id=camera_id,
            confidence=0.95,
        )
    )

    if not person_result.accepted:

        return _result(
            success=False,
            action="AUTHENTICATE",
            message=person_result.message,
            stage="AUTHENTICATION_REJECTED",
        )

    active_sessions = (
        authentication_service
        .get_active_sessions()
    )

    if not active_sessions:

        return _result(
            success=False,
            action="AUTHENTICATE",
            message=(
                "Authentication session "
                "could not be created."
            ),
            stage="AUTHENTICATION_FAILED",
        )

    latest = max(
        active_sessions,
        key=lambda session: (
            session.updated_at
            or datetime.min.replace(
                tzinfo=timezone.utc
            )
        ),
    )

    session_id = latest.session_id

    if method == AuthenticationMethod.FACE:

        auth_result = (
            authentication_service
            .face_recognized(
                session_id=session_id,
                student_id=str(student_id),
                confidence=0.98,
                recognized=True,
            )
        )

    elif method == AuthenticationMethod.QR:

        auth_result = (
            authentication_service
            .qr_scanned(
                session_id=session_id,
                student_id=str(student_id),
                valid=True,
            )
        )

    else:

        return _result(
            success=False,
            action="AUTHENTICATE",
            message="Unsupported authentication method.",
            stage="AUTHENTICATION_FAILED",
            session_id=session_id,
        )

    if not auth_result.accepted:

        return _result(
            success=False,
            action="AUTHENTICATE",
            message=auth_result.message,
            stage="AUTHENTICATION_REJECTED",
            session_id=session_id,
            authentication=_serialize(
                auth_result
            ),
        )

    if not auth_result.authenticated:

        return _result(
            success=False,
            action="AUTHENTICATE",
            message=auth_result.message,
            stage="AUTHENTICATION_FAILED",
            session_id=session_id,
            authentication=_serialize(
                auth_result
            ),
        )

    _get_or_create_simulation_session(
        authentication_session_id=session_id,
        student_id=str(student_id),
        camera_id=camera_id,
        authentication_method=method.value,
    )

    return _result(
        success=True,
        action="AUTHENTICATE",
        message="Student authenticated successfully.",
        stage="AUTHENTICATED",
        session_id=session_id,
        student_id=str(student_id),
        authentication_method=method.value,
        authentication=_serialize(
            auth_result
        ),
    )


# ============================================================
# ENTRY
# ============================================================

def simulate_entry(
    db: Session,
    authentication_session_id: str,
    student_id: str,
):

    auth_session = (
        authentication_service
        .get_session(
            authentication_session_id
        )
    )

    if auth_session is None:

        return _result(
            success=False,
            action="ENTRY",
            message="Authentication session not found.",
            stage="ENTRY_REJECTED",
        )

    if not auth_session.authenticated:

        return _result(
            success=False,
            action="ENTRY",
            message="Student is not authenticated.",
            stage="ENTRY_REJECTED",
            session_id=authentication_session_id,
        )

    if str(auth_session.student_id) != str(student_id):

        return _result(
            success=False,
            action="ENTRY",
            message=(
                "Authenticated student does not "
                "match entry student."
            ),
            stage="ENTRY_REJECTED",
            session_id=authentication_session_id,
        )

    # --------------------------------------------------------
    # Prevent duplicate DB entry
    # --------------------------------------------------------

    existing_attendance = _get_active_attendance(
        student_id=student_id,
        db=db,
    )

    if existing_attendance:

        return _result(
            success=False,
            action="ENTRY",
            message="Student is already inside the lab.",
            stage="ENTRY_REJECTED",
            student_id=str(student_id),
            session_id=authentication_session_id,
            attendance_id=_serialize(
                existing_attendance.attendance_id
            ),
        )

    # --------------------------------------------------------
    # ATTENDANCE IN
    # --------------------------------------------------------

    attendance = check_in(
        student_id=str(student_id),
        db=db,
    )

    # --------------------------------------------------------
    # LAB SESSION START
    # --------------------------------------------------------

    lab_session = start_session(
        student_id=str(student_id),
        attendance_id=attendance.attendance_id,
        db=db,
    )

    simulation_data = (
        _get_or_create_simulation_session(
            authentication_session_id=(
                authentication_session_id
            ),
            student_id=str(student_id),
            camera_id=auth_session.camera_id,
            authentication_method=(
                auth_session.method.value
                if auth_session.method
                else "NONE"
            ),
        )
    )

    simulation_data.update(
        {
            "entry": utc_now(),
            "attendance_id": attendance.attendance_id,
            "lab_session_id": lab_session.session_id,
            "completed": False,
        }
    )

    return _result(
        success=True,
        action="ENTRY",
        message="Student entered the lab successfully.",
        stage="LAB_ACTIVE",
        student_id=str(student_id),
        session_id=authentication_session_id,
        attendance_id=_serialize(
            attendance.attendance_id
        ),
        lab_session_id=_serialize(
            lab_session.session_id
        ),
        camera_id=auth_session.camera_id,
        entry_time=_serialize(
            attendance.entry_time
        ),
    )


# ============================================================
# TAKE COMPONENT
# ============================================================

def simulate_take(
    db: Session,
    student_id: str,
    component_id: str,
    quantity: int = 1,
):

    authenticated_session = (
        _find_authenticated_session(
            student_id
        )
    )

    if authenticated_session is None:

        return _result(
            success=False,
            action="TAKE",
            message=(
                "Student must be authenticated "
                "before taking a component."
            ),
            stage="TAKE_REJECTED",
            student_id=str(student_id),
        )

    # --------------------------------------------------------
    # DATABASE IS SOURCE OF TRUTH FOR LAB ENTRY
    # --------------------------------------------------------

    active_lab_session = _get_active_lab_session(
        student_id=student_id,
        db=db,
    )

    if active_lab_session is None:

        return _result(
            success=False,
            action="TAKE",
            message="Student has not entered the lab.",
            stage="TAKE_REJECTED",
            student_id=str(student_id),
            session_id=(
                authenticated_session.session_id
            ),
        )

    simulation_data = (
        simulation_sessions.get(
            authenticated_session.session_id
        )
    )

    if simulation_data is None:

        simulation_data = (
            _get_or_create_simulation_session(
                authentication_session_id=(
                    authenticated_session.session_id
                ),
                student_id=str(student_id),
                camera_id=authenticated_session.camera_id,
                authentication_method=(
                    authenticated_session.method.value
                    if authenticated_session.method
                    else "NONE"
                ),
            )
        )

    simulation_data["lab_session_id"] = (
        active_lab_session.session_id
    )

    # --------------------------------------------------------
    # CREATE PENDING TRANSACTION
    # --------------------------------------------------------

    transaction = create_take_transaction(
        db=db,
        student_id=str(student_id),
        component_id=component_id,
        quantity=quantity,
    )

    simulation_data.setdefault(
        "transactions",
        [],
    ).append(
        transaction.transaction_id
    )

    return _result(
        success=True,
        action="TAKE",
        message=(
            "Component TAKE request created. "
            "Waiting for Camera 2 verification."
        ),
        stage="WAITING_FOR_CAMERA_2",
        student_id=str(student_id),
        session_id=(
            authenticated_session.session_id
        ),
        transaction_id=_serialize(
            transaction.transaction_id
        ),
        component_id=component_id,
        quantity=quantity,
        camera_id="camera_2",
        verification_status=(
            transaction.verification_status
        ),
        transaction_status=(
            transaction.status
        ),
        transaction=_serialize(
            transaction
        ),
    )


# ============================================================
# CAMERA 2 MATCH
# ============================================================

def simulate_match(
    db: Session,
    transaction_id: str,
    expected_component: str,
    confidence: float = 0.95,
    camera_id: str = "camera_2",
):

    try:

        transaction_uuid = uuid.UUID(
            str(transaction_id)
        )

    except (
        ValueError,
        TypeError,
        AttributeError,
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid transaction_id.",
        )

    transaction = get_transaction(
        db=db,
        transaction_id=transaction_uuid,
    )

    if transaction is None:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found.",
        )

    verified = verify_transaction(
        db=db,
        transaction_id=transaction_uuid,
        detected_component=expected_component,
        camera_id=camera_id,
        confidence=confidence,
    )

    success = (
        verified.verification_status == "MATCHED"
        and verified.status
        in [
            "APPROVED",
            "COMPLETED",
        ]
    )

    return _result(
        success=success,
        action="VERIFY_MATCH",
        message=(
            "Camera 2 verification matched. "
            "Transaction approved."
            if success
            else
            "Camera 2 verification did not "
            "approve the transaction."
        ),
        stage=(
            "TRANSACTION_APPROVED"
            if success
            else "TRANSACTION_REJECTED"
        ),
        transaction_id=_serialize(
            verified.transaction_id
        ),
        component_id=verified.component_id,
        camera_id=camera_id,
        detected_component=expected_component,
        confidence=confidence,
        verification_status=(
            verified.verification_status
        ),
        transaction_status=verified.status,
        inventory_updated=success,
        transaction=_serialize(
            verified
        ),
    )


# ============================================================
# CAMERA 2 MISMATCH
# ============================================================

def simulate_mismatch(
    db: Session,
    transaction_id: str,
    expected_component: str,
    detected_component: str,
    confidence: float = 0.95,
    camera_id: str = "camera_2",
):

    try:

        transaction_uuid = uuid.UUID(
            str(transaction_id)
        )

    except (
        ValueError,
        TypeError,
        AttributeError,
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid transaction_id.",
        )

    transaction = get_transaction(
        db=db,
        transaction_id=transaction_uuid,
    )

    if transaction is None:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found.",
        )

    verified = verify_transaction(
        db=db,
        transaction_id=transaction_uuid,
        detected_component=detected_component,
        camera_id=camera_id,
        confidence=confidence,
    )

    alert_result = simulate_component_mismatch(
        db=db,
        camera_id=camera_id,
        component_id=verified.component_id,
        expected_component=expected_component,
        detected_component=detected_component,
        student_id=None,
        confidence=confidence,
        transaction_id=verified.transaction_id,
    )

    return _result(
        success=False,
        action="VERIFY_MISMATCH",
        message=(
            "Component mismatch detected. "
            "Transaction rejected and alert generated."
        ),
        stage="MISMATCH_REJECTED",
        transaction_id=_serialize(
            verified.transaction_id
        ),
        component_id=verified.component_id,
        camera_id=camera_id,
        detected_component=detected_component,
        expected_component=expected_component,
        confidence=confidence,
        verification_status=(
            verified.verification_status
        ),
        transaction_status=verified.status,
        inventory_updated=False,
        alert_created=True,
        transaction=_serialize(
            verified
        ),
        alert=_serialize(
            alert_result
        ),
    )


# ============================================================
# EXIT
# ============================================================

def simulate_exit(
    db: Session,
    authentication_session_id: Optional[str],
    student_id: str,
):

    # --------------------------------------------------------
    # AUTHENTICATION
    #
    # Authentication is required, but the old simulation
    # dictionary is NOT required.
    # --------------------------------------------------------

    if authentication_session_id:

        auth_session = (
            authentication_service
            .get_session(
                authentication_session_id
            )
        )

        if auth_session is None:

            return _result(
                success=False,
                action="EXIT",
                message="Authentication session not found.",
                stage="EXIT_REJECTED",
            )

        if not auth_session.authenticated:

            return _result(
                success=False,
                action="EXIT",
                message="Student is not authenticated.",
                stage="EXIT_REJECTED",
                session_id=authentication_session_id,
            )

        if (
            str(auth_session.student_id)
            != str(student_id)
        ):

            return _result(
                success=False,
                action="EXIT",
                message=(
                    "Authenticated student does not "
                    "match exit student."
                ),
                stage="EXIT_REJECTED",
                session_id=authentication_session_id,
            )

    # --------------------------------------------------------
    # DATABASE SOURCE OF TRUTH
    #
    # This is the critical fix.
    #
    # Even if Uvicorn restarted and erased:
    #
    # simulation_sessions
    #
    # the database still contains:
    #
    # Attendance = IN
    # LabSession = ACTIVE
    #
    # --------------------------------------------------------

    active_attendance = _get_active_attendance(
        student_id=student_id,
        db=db,
    )

    if active_attendance is None:

        return _result(
            success=False,
            action="EXIT",
            message="No active attendance found.",
            stage="EXIT_REJECTED",
            student_id=str(student_id),
            session_id=authentication_session_id,
        )

    active_lab_session = _get_active_lab_session(
        student_id=student_id,
        db=db,
    )

    if active_lab_session is None:

        return _result(
            success=False,
            action="EXIT",
            message="No active lab session found.",
            stage="EXIT_REJECTED",
            student_id=str(student_id),
            session_id=authentication_session_id,
            attendance_id=_serialize(
                active_attendance.attendance_id
            ),
        )

    # --------------------------------------------------------
    # EXPLICIT ATTENDANCE EXIT
    # --------------------------------------------------------

    attendance = check_out(
        student_id=str(student_id),
        db=db,
    )

    # --------------------------------------------------------
    # EXPLICIT LAB SESSION END
    # --------------------------------------------------------

    lab_session = end_session(
        student_id=str(student_id),
        db=db,
    )

    exit_time = utc_now()

    # --------------------------------------------------------
    # Update runtime state if it still exists.
    #
    # This is optional. Database state above is authoritative.
    # --------------------------------------------------------

    if authentication_session_id:

        simulation_data = (
            simulation_sessions.get(
                authentication_session_id
            )
        )

        if simulation_data:

            simulation_data.update(
                {
                    "exit": exit_time,
                    "completed": True,
                }
            )

    return _result(
        success=True,
        action="EXIT",
        message=(
            "Student exited the lab successfully. "
            "Attendance and lab session completed."
        ),
        stage="LAB_COMPLETED",
        student_id=str(student_id),
        session_id=authentication_session_id,
        attendance_id=_serialize(
            getattr(
                attendance,
                "attendance_id",
                None,
            )
        ),
        lab_session_id=_serialize(
            getattr(
                lab_session,
                "session_id",
                None,
            )
        ),
        exit_time=_serialize(
            getattr(
                attendance,
                "exit_time",
                None,
            )
        ),
        attendance=_serialize(
            attendance
        ),
        lab_session=_serialize(
            lab_session
        ),
    )


# ============================================================
# FULL END-TO-END SIMULATION
# ============================================================

def simulate_full_flow(
    db: Session,
    student_id: str,
    component_id: str,
    quantity: int = 1,
    authentication_method: str = "FACE",
    camera_1: str = "camera_1",
    camera_2: str = "camera_2",
    verification_mode: str = "MATCH",
    confidence: float = 0.95,
):

    steps = []

    # ========================================================
    # 1. AUTHENTICATION
    # ========================================================

    authentication = simulate_authentication(
        db=db,
        student_id=student_id,
        authentication_method=authentication_method,
        camera_id=camera_1,
    )

    steps.append(authentication)

    if not authentication["success"]:

        return {
            "success": False,
            "message": (
                "Full simulation stopped "
                "during authentication."
            ),
            "student_id": str(student_id),
            "session_id": None,
            "transaction_id": None,
            "verification_status": None,
            "inventory_updated": False,
            "alert_created": False,
            "steps": steps,
        }

    session_id = authentication[
        "session_id"
    ]

    # ========================================================
    # 2. ENTRY
    # ========================================================

    entry = simulate_entry(
        db=db,
        authentication_session_id=session_id,
        student_id=student_id,
    )

    steps.append(entry)

    if not entry["success"]:

        return {
            "success": False,
            "message": (
                "Full simulation stopped "
                "during lab entry."
            ),
            "student_id": str(student_id),
            "attendance_id": entry.get(
                "attendance_id"
            ),
            "session_id": session_id,
            "transaction_id": None,
            "verification_status": None,
            "inventory_updated": False,
            "alert_created": False,
            "steps": steps,
        }

    # ========================================================
    # 3. TAKE
    # ========================================================

    take = simulate_take(
        db=db,
        student_id=student_id,
        component_id=component_id,
        quantity=quantity,
    )

    steps.append(take)

    if not take["success"]:

        return {
            "success": False,
            "message": (
                "Full simulation stopped "
                "during component TAKE."
            ),
            "student_id": str(student_id),
            "attendance_id": entry.get(
                "attendance_id"
            ),
            "session_id": session_id,
            "transaction_id": None,
            "verification_status": None,
            "inventory_updated": False,
            "alert_created": False,
            "steps": steps,
        }

    transaction_id = take[
        "transaction_id"
    ]

    # ========================================================
    # 4. CAMERA 2 VERIFICATION
    # ========================================================

    mode = str(
        verification_mode
    ).upper()

    if mode in [
        "MATCH",
        "MATCHED",
        "PASS",
    ]:

        verification = simulate_match(
            db=db,
            transaction_id=transaction_id,
            expected_component=component_id,
            confidence=confidence,
            camera_id=camera_2,
        )

    elif mode in [
        "MISMATCH",
        "FAIL",
        "FAILED",
    ]:

        verification = simulate_mismatch(
            db=db,
            transaction_id=transaction_id,
            expected_component=component_id,
            detected_component="Arduino UNO",
            confidence=confidence,
            camera_id=camera_2,
        )

    else:

        raise HTTPException(
            status_code=400,
            detail=(
                "verification_mode must be "
                "MATCH or MISMATCH."
            ),
        )

    steps.append(verification)

    # ========================================================
    # 5. EXIT ONLY AFTER SUCCESSFUL VERIFICATION
    # ========================================================

    exit_result = None

    if verification["success"]:

        exit_result = simulate_exit(
            db=db,
            authentication_session_id=session_id,
            student_id=student_id,
        )

        steps.append(exit_result)

    # ========================================================
    # FINAL STATUS
    # ========================================================

    overall_success = (
        authentication["success"]
        and entry["success"]
        and take["success"]
        and verification["success"]
        and exit_result is not None
        and exit_result["success"]
    )

    return {
        "success": overall_success,
        "message": (
            "Complete SmartLab workflow "
            "executed successfully."
            if overall_success
            else
            "SmartLab workflow stopped at verification."
        ),
        "student_id": str(student_id),
        "attendance_id": (
            entry.get("attendance_id")
            if entry
            else None
        ),
        "session_id": session_id,
        "transaction_id": transaction_id,
        "verification_status": (
            verification.get(
                "verification_status"
            )
        ),
        "inventory_updated": (
            verification.get(
                "inventory_updated",
                False,
            )
        ),
        "alert_created": (
            verification.get(
                "alert_created",
                False,
            )
        ),
        "steps": steps,
    }