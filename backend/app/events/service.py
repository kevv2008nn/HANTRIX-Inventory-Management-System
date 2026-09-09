from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.alerts.service import (
    create_mismatch_alert,
    create_system_warning_if_new,
    create_unknown_person_alert,
)

from app.authentication.service import (
    authentication_service,
)

from app.events.schemas import (
    EventResult,
    SmartLabEvent,
)


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


EVENT_SEVERITIES = {
    "INFO",
    "WARNING",
    "HIGH",
    "CRITICAL",
}


# ============================================================
# TIME
# ============================================================

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# ============================================================
# VALIDATION
# ============================================================

def validate_event(event: SmartLabEvent) -> None:

    event_type = str(
        event.event_type
    ).strip().upper()

    if event_type not in EVENT_TYPES:
        raise ValueError(
            f"Unsupported event type: {event_type}"
        )

    severity = str(
        getattr(
            event,
            "severity",
            None,
        )
        or "INFO"
    ).strip().upper()

    if severity not in EVENT_SEVERITIES:
        raise ValueError(
            f"Unsupported event severity: {severity}"
        )


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_event(
    event: SmartLabEvent,
) -> SmartLabEvent:

    event.event_type = (
        str(event.event_type)
        .strip()
        .upper()
    )

    if getattr(event, "source", None):

        event.source = (
            str(event.source)
            .strip()
            .upper()
        )

    if getattr(event, "camera_id", None):

        event.camera_id = (
            str(event.camera_id)
            .strip()
        )

    event.severity = (
        str(
            getattr(
                event,
                "severity",
                None,
            )
            or "INFO"
        )
        .strip()
        .upper()
    )

    if getattr(event, "student_id", None):

        event.student_id = (
            str(event.student_id)
            .strip()
        )

    if getattr(event, "component_id", None):

        event.component_id = (
            str(event.component_id)
            .strip()
        )

    if getattr(event, "transaction_id", None):

        event.transaction_id = (
            str(event.transaction_id)
            .strip()
        )

    return event


# ============================================================
# PERSON DETECTED
# ============================================================

def handle_person_detected(
    event: SmartLabEvent,
) -> EventResult:
    """
    Starts an authentication session when Camera 1
    detects a person.

    This is the bridge:

        Camera 1
             ↓
        PERSON_DETECTED
             ↓
        AuthenticationService
             ↓
        AUTHENTICATING
    """

    camera_id = (
        getattr(
            event,
            "camera_id",
            None,
        )
        or "camera_1"
    )

    # --------------------------------------------------------
    # CAMERA VALIDATION
    # --------------------------------------------------------

    if str(camera_id).lower() != "camera_1":

        return EventResult(
            accepted=False,
            event_type="PERSON_DETECTED",
            message=(
                "PERSON_DETECTED events must "
                "come from camera_1."
            ),
            processed_at=utc_now(),
        )

    confidence = getattr(
        event,
        "confidence",
        None,
    )

    # --------------------------------------------------------
    # START AUTHENTICATION
    # --------------------------------------------------------

    result = authentication_service.person_detected(
        camera_id=str(camera_id),
        confidence=confidence,
    )

    # --------------------------------------------------------
    # FIND NEWEST AUTHENTICATION SESSION
    # --------------------------------------------------------

    active_sessions = (
        authentication_service
        .get_active_sessions()
    )

    matching_sessions = [
        session
        for session in active_sessions
        if session.camera_id == str(camera_id)
    ]

    session_id = None
    authentication_state = None

    if matching_sessions:

        newest_session = max(
            matching_sessions,
            key=lambda session: session.updated_at,
        )

        session_id = (
            newest_session.session_id
        )

        authentication_state = (
            str(newest_session.state)
        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return EventResult(
        accepted=result.accepted,
        event_type="PERSON_DETECTED",
        message=result.message,
        session_id=session_id,
        authentication_state=authentication_state,
        authenticated=result.authenticated,
        student_id=result.student_id,
        alert_created=False,
        alert_id=None,
        processed_at=utc_now(),
    )


# ============================================================
# UNKNOWN PERSON
# ============================================================

def handle_unknown_person(
    db: Session,
    event: SmartLabEvent,
) -> EventResult:

    camera_id = getattr(
        event,
        "camera_id",
        None,
    )

    confidence = getattr(
        event,
        "confidence",
        None,
    )

    alert = create_unknown_person_alert(
        db=db,
        camera_id=camera_id,
        confidence=confidence,
    )

    return EventResult(
        accepted=True,
        event_type="UNKNOWN_PERSON",
        message=(
            "Unknown person detected "
            "and alert created."
        ),
        alert_created=True,
        alert_id=(
            str(alert.alert_id)
            if alert
            else None
        ),
        processed_at=utc_now(),
    )


# ============================================================
# COMPONENT MISMATCH
# ============================================================

def handle_component_mismatch(
    db: Session,
    event: SmartLabEvent,
) -> EventResult:

    data = (
        getattr(
            event,
            "data",
            None,
        )
        or {}
    )

    expected_component = (
        data.get(
            "expected_component"
        )
        or getattr(
            event,
            "expected_component",
            None,
        )
    )

    detected_component = (
        data.get(
            "detected_component"
        )
        or getattr(
            event,
            "detected_component",
            None,
        )
    )

    component_id = (
        getattr(
            event,
            "component_id",
            None,
        )
        or data.get(
            "component_id"
        )
    )

    camera_id = (
        getattr(
            event,
            "camera_id",
            None,
        )
        or data.get(
            "camera_id"
        )
    )

    student_id = (
        getattr(
            event,
            "student_id",
            None,
        )
        or data.get(
            "student_id"
        )
    )

    confidence = getattr(
        event,
        "confidence",
        None,
    )

    if confidence is None:

        confidence = data.get(
            "confidence"
        )

    transaction_id = (
        getattr(
            event,
            "transaction_id",
            None,
        )
        or data.get(
            "transaction_id"
        )
    )

    # --------------------------------------------------------
    # REQUIRED FIELDS
    # --------------------------------------------------------

    if not expected_component:

        raise ValueError(
            "COMPONENT_MISMATCH requires "
            "expected_component."
        )

    if not detected_component:

        raise ValueError(
            "COMPONENT_MISMATCH requires "
            "detected_component."
        )

    if not component_id:

        raise ValueError(
            "COMPONENT_MISMATCH requires "
            "component_id."
        )

    # --------------------------------------------------------
    # TRANSACTION UUID
    # --------------------------------------------------------

    transaction_uuid: Optional[UUID] = None

    if transaction_id:

        try:

            transaction_uuid = UUID(
                str(transaction_id)
            )

        except (
            ValueError,
            TypeError,
            AttributeError,
        ):

            raise ValueError(
                "transaction_id must be "
                "a valid UUID."
            )

    # --------------------------------------------------------
    # STUDENT ID
    # --------------------------------------------------------

    if student_id is not None:

        student_id = str(
            student_id
        ).strip()

        if not student_id:

            student_id = None

    # --------------------------------------------------------
    # CREATE ALERT
    # --------------------------------------------------------

    alert = create_mismatch_alert(
        db=db,
        student_id=student_id,
        component_id=str(
            component_id
        ),
        transaction_id=transaction_uuid,
        camera_id=camera_id,
        expected_component=str(
            expected_component
        ),
        detected_component=str(
            detected_component
        ),
        confidence=confidence,
    )

    return EventResult(
        accepted=True,
        event_type="COMPONENT_MISMATCH",
        message=(
            f"Component mismatch detected: "
            f"expected '{expected_component}' "
            f"but detected "
            f"'{detected_component}'."
        ),
        alert_created=True,
        alert_id=(
            str(alert.alert_id)
            if alert
            else None
        ),
        processed_at=utc_now(),
    )


# ============================================================
# SYSTEM WARNING
# ============================================================

def handle_system_warning(
    db: Session,
    event: SmartLabEvent,
) -> EventResult:

    data = (
        getattr(
            event,
            "data",
            None,
        )
        or {}
    )

    title = (
        data.get("title")
        or getattr(
            event,
            "title",
            None,
        )
        or "SmartLab System Warning"
    )

    message = (
        data.get("message")
        or getattr(
            event,
            "message",
            None,
        )
        or (
            "A SmartLab system warning "
            "was generated."
        )
    )

    severity = (
        data.get("severity")
        or getattr(
            event,
            "severity",
            None,
        )
        or "WARNING"
    )

    camera_id = (
        data.get("camera_id")
        or getattr(
            event,
            "camera_id",
            None,
        )
    )

    metadata = data.get(
        "metadata"
    )

    alert = create_system_warning_if_new(
        db=db,
        title=str(title),
        message=str(message),
        severity=str(
            severity
        ).upper(),
        camera_id=camera_id,
        metadata=metadata,
    )

    if alert:

        return EventResult(
            accepted=True,
            event_type="SYSTEM_WARNING",
            message=(
                "System warning alert created."
            ),
            alert_created=True,
            alert_id=str(
                alert.alert_id
            ),
            processed_at=utc_now(),
        )

    return EventResult(
        accepted=True,
        event_type="SYSTEM_WARNING",
        message=(
            "Duplicate system warning ignored."
        ),
        alert_created=False,
        alert_id=None,
        processed_at=utc_now(),
    )


# ============================================================
# INFORMATION EVENTS
# ============================================================

def handle_information_event(
    event: SmartLabEvent,
) -> EventResult:

    messages = {

        "FACE_RECOGNIZED":
            "Face recognition event received.",

        "QR_SCANNED":
            "QR scan event received.",

        "PERSON_ENTERED":
            "Person entry event received.",

        "PERSON_EXITED":
            "Person exit event received.",

        "ATTENDANCE_MARKED":
            "Attendance event received.",

        "SESSION_STARTED":
            "Lab session start event received.",

        "SESSION_ENDED":
            "Lab session end event received.",

        "TRANSACTION_CREATED":
            "Transaction creation event received.",

        "TRANSACTION_VERIFIED":
            "Transaction verification event received.",

        "TRANSACTION_APPROVED":
            "Transaction approval event received.",

        "TRANSACTION_REJECTED":
            "Transaction rejection event received.",

        "COMPONENT_DETECTED":
            "Component detection event received.",

        "COMPONENT_PICKED":
            "Component pickup event received.",

        "COMPONENT_RETURNED":
            "Component return event received.",

        "LOW_STOCK":
            "Low-stock event received.",

        "OVERDUE":
            "Overdue transaction event received.",

        "CAMERA_ONLINE":
            "Camera online event received.",

        "CAMERA_OFFLINE":
            "Camera offline event received.",

        "SYSTEM_ERROR":
            "System error event received.",
    }

    event_type = str(
        event.event_type
    ).upper()

    return EventResult(
        accepted=True,
        event_type=event_type,
        message=messages.get(
            event_type,
            "SmartLab event received.",
        ),
        processed_at=utc_now(),
    )


# ============================================================
# MAIN EVENT PROCESSOR
# ============================================================

def process_event(
    db: Session,
    event: SmartLabEvent,
) -> EventResult:

    validate_event(event)

    event = normalize_event(event)

    event_type = str(
        event.event_type
    ).upper()

    # --------------------------------------------------------
    # PERSON DETECTED
    # --------------------------------------------------------

    if event_type == "PERSON_DETECTED":

        return handle_person_detected(
            event=event,
        )

    # --------------------------------------------------------
    # UNKNOWN PERSON
    # --------------------------------------------------------

    if event_type == "UNKNOWN_PERSON":

        return handle_unknown_person(
            db=db,
            event=event,
        )

    # --------------------------------------------------------
    # COMPONENT MISMATCH
    # --------------------------------------------------------

    if event_type == "COMPONENT_MISMATCH":

        return handle_component_mismatch(
            db=db,
            event=event,
        )

    # --------------------------------------------------------
    # SYSTEM WARNING
    # --------------------------------------------------------

    if event_type == "SYSTEM_WARNING":

        return handle_system_warning(
            db=db,
            event=event,
        )

    # --------------------------------------------------------
    # INFORMATION EVENTS
    # --------------------------------------------------------

    return handle_information_event(
        event
    )


# ============================================================
# SIMULATION: PERSON DETECTED
# ============================================================

def simulate_person_detected(
    db: Session,
    camera_id: str = "camera_1",
    confidence: float = 0.95,
) -> EventResult:

    event = SmartLabEvent(
        event_type="PERSON_DETECTED",
        source="SIMULATOR",
        camera_id=camera_id,
        confidence=confidence,
        severity="INFO",
        data={
            "simulation": True,
        },
    )

    return process_event(
        db=db,
        event=event,
    )


# ============================================================
# SIMULATION: UNKNOWN PERSON
# ============================================================

def simulate_unknown_person(
    db: Session,
    camera_id: str = "camera_1",
    confidence: float = 0.87,
) -> EventResult:

    event = SmartLabEvent(
        event_type="UNKNOWN_PERSON",
        source="SIMULATOR",
        camera_id=camera_id,
        confidence=confidence,
        severity="HIGH",
        data={
            "simulation": True,
        },
    )

    return process_event(
        db=db,
        event=event,
    )


# ============================================================
# SIMULATION: COMPONENT MISMATCH
# ============================================================

def simulate_component_mismatch(
    db: Session,
    camera_id: str = "camera_2",
    component_id: str = "ESP32-001",
    expected_component: str = "ESP32",
    detected_component: str = "Arduino UNO",
    student_id: Optional[str] = None,
    confidence: float = 0.94,
    transaction_id: Optional[str] = None,
) -> EventResult:

    event = SmartLabEvent(
        event_type="COMPONENT_MISMATCH",
        source="SIMULATOR",
        camera_id=camera_id,
        student_id=student_id,
        component_id=component_id,
        transaction_id=transaction_id,
        confidence=confidence,
        severity="CRITICAL",
        data={
            "simulation": True,
            "expected_component":
                expected_component,
            "detected_component":
                detected_component,
            "component_id":
                component_id,
            "camera_id":
                camera_id,
            "student_id":
                student_id,
            "transaction_id":
                transaction_id,
            "confidence":
                confidence,
        },
    )

    return process_event(
        db=db,
        event=event,
    )


# ============================================================
# SIMULATION: SYSTEM WARNING
# ============================================================

def simulate_system_warning(
    db: Session,
    title: str = "AI Engine Warning",
    message: str = (
        "The simulated AI engine "
        "reported a warning."
    ),
    severity: str = "WARNING",
    camera_id: Optional[str] = None,
) -> EventResult:

    event = SmartLabEvent(
        event_type="SYSTEM_WARNING",
        source="SIMULATOR",
        camera_id=camera_id,
        severity=severity.upper(),
        data={
            "simulation": True,
            "title": title,
            "message": message,
            "severity": severity.upper(),
            "camera_id": camera_id,
            "metadata": {
                "simulation": True,
            },
        },
    )

    return process_event(
        db=db,
        event=event,
    )