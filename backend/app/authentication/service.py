import uuid
from datetime import datetime, timezone
from typing import Dict, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.authentication.schemas import (
    AuthenticationMethod,
    AuthenticationResult,
    AuthenticationSession,
    AuthenticationState,
    AuthenticationActionResult,
    LabAction,
)

from app.alerts.service import create_unknown_person_alert
from app.attendance.service import check_in, check_out
from app.lab_sessions.service import start_session, end_session


class AuthenticationService:
    """
    Runtime authentication state machine.

    Camera / AI / QR systems provide:
        - person detected
        - face recognition result
        - QR result

    This service maintains authentication state and controls
    authenticated ENTRY / EXIT actions.
    """

    def __init__(self):
        self.sessions: Dict[str, AuthenticationSession] = {}

    # =========================================================
    # INTERNAL
    # =========================================================

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _create_session(
        self,
        camera_id: str,
    ) -> AuthenticationSession:

        session_id = str(uuid.uuid4())

        session = AuthenticationSession(
            session_id=session_id,
            camera_id=camera_id,
            state=AuthenticationState.IDLE,
            method=AuthenticationMethod.NONE,
        )

        self.sessions[session_id] = session

        return session

    def _update(
        self,
        session: AuthenticationSession,
        **kwargs,
    ) -> AuthenticationSession:

        updated = session.model_copy(
            update={
                **kwargs,
                "updated_at": self._now(),
            }
        )

        self.sessions[session.session_id] = updated

        return updated

    # =========================================================
    # GET SESSION
    # =========================================================

    def get_session(
        self,
        session_id: str,
    ) -> Optional[AuthenticationSession]:

        return self.sessions.get(session_id)

    # =========================================================
    # PERSON DETECTED
    # =========================================================

    def person_detected(
        self,
        camera_id: str,
        confidence: Optional[float] = None,
    ) -> AuthenticationResult:

        session = self._create_session(
            camera_id=camera_id
        )

        session = self._update(
            session,
            state=AuthenticationState.PERSON_DETECTED,
            confidence=confidence,
        )

        session = self._update(
            session,
            state=AuthenticationState.AUTHENTICATING,
        )

        return AuthenticationResult(
            accepted=True,
            state=session.state,
            authenticated=False,
            unknown=False,
            student_id=None,
            method=AuthenticationMethod.NONE,
            confidence=confidence,
            message="Person detected. Authentication started.",
            updated_at=session.updated_at,
        )

    # =========================================================
    # FACE RECOGNITION
    # =========================================================

    def face_recognized(
        self,
        session_id: str,
        student_id: Optional[str],
        confidence: float,
        recognized: bool,
        db: Optional[Session] = None,
    ) -> AuthenticationResult:

        session = self.get_session(session_id)

        if session is None:

            return AuthenticationResult(
                accepted=False,
                state=AuthenticationState.REJECTED,
                authenticated=False,
                unknown=False,
                message="Authentication session not found.",
            )

        if session.state not in (
            AuthenticationState.AUTHENTICATING,
            AuthenticationState.FACE_RECOGNIZED,
            AuthenticationState.QR_SCANNED,
        ):

            return AuthenticationResult(
                accepted=False,
                state=AuthenticationState.REJECTED,
                authenticated=False,
                unknown=False,
                student_id=session.student_id,
                method=session.method,
                confidence=session.confidence,
                message=(
                    f"Invalid state transition from "
                    f"{session.state}."
                ),
            )

        # -----------------------------------------------------
        # UNKNOWN FACE
        # -----------------------------------------------------

        if not recognized or not student_id:

            session = self._update(
                session,
                state=AuthenticationState.UNKNOWN,
                method=AuthenticationMethod.FACE,
                confidence=confidence,
                authenticated=False,
                unknown=True,
                student_id=None,
            )

            # Create security alert when DB is available
            if db is not None:

                try:

                    create_unknown_person_alert(
                        db=db,
                        camera_id=session.camera_id or "camera_1",
                        confidence=confidence,
                    )

                except Exception:
                    # Authentication state must not be lost
                    # just because alert creation failed.
                    db.rollback()

            return AuthenticationResult(
                accepted=True,
                state=AuthenticationState.UNKNOWN,
                authenticated=False,
                unknown=True,
                student_id=None,
                method=AuthenticationMethod.FACE,
                confidence=confidence,
                message=(
                    "Face detected but student could not "
                    "be authenticated."
                ),
                updated_at=session.updated_at,
            )

        # -----------------------------------------------------
        # KNOWN FACE
        # -----------------------------------------------------

        session = self._update(
            session,
            state=AuthenticationState.FACE_RECOGNIZED,
            method=AuthenticationMethod.FACE,
            confidence=confidence,
            student_id=student_id,
        )

        session = self._update(
            session,
            state=AuthenticationState.AUTHENTICATED,
            authenticated=True,
            unknown=False,
        )

        return AuthenticationResult(
            accepted=True,
            state=AuthenticationState.AUTHENTICATED,
            authenticated=True,
            unknown=False,
            student_id=student_id,
            method=AuthenticationMethod.FACE,
            confidence=confidence,
            message=(
                "Student authenticated successfully "
                "using face recognition."
            ),
            updated_at=session.updated_at,
        )

    # =========================================================
    # QR AUTHENTICATION
    # =========================================================

    def qr_scanned(
        self,
        session_id: str,
        student_id: Optional[str],
        valid: bool,
        db: Optional[Session] = None,
    ) -> AuthenticationResult:

        session = self.get_session(session_id)

        if session is None:

            return AuthenticationResult(
                accepted=False,
                state=AuthenticationState.REJECTED,
                authenticated=False,
                unknown=False,
                message="Authentication session not found.",
            )

        if session.state != AuthenticationState.AUTHENTICATING:

            return AuthenticationResult(
                accepted=False,
                state=AuthenticationState.REJECTED,
                authenticated=False,
                unknown=False,
                student_id=session.student_id,
                method=session.method,
                confidence=session.confidence,
                message=(
                    f"QR authentication is not allowed from "
                    f"state {session.state}."
                ),
            )

        # -----------------------------------------------------
        # INVALID QR
        # -----------------------------------------------------

        if not valid or not student_id:

            session = self._update(
                session,
                state=AuthenticationState.UNKNOWN,
                method=AuthenticationMethod.QR,
                authenticated=False,
                unknown=True,
                student_id=None,
            )

            # Invalid/unknown QR also creates security alert
            if db is not None:

                try:

                    create_unknown_person_alert(
                        db=db,
                        camera_id=session.camera_id or "camera_1",
                        confidence=None,
                    )

                except Exception:
                    db.rollback()

            return AuthenticationResult(
                accepted=True,
                state=AuthenticationState.UNKNOWN,
                authenticated=False,
                unknown=True,
                student_id=None,
                method=AuthenticationMethod.QR,
                confidence=None,
                message="QR code is invalid or student is unknown.",
                updated_at=session.updated_at,
            )

        # -----------------------------------------------------
        # VALID QR
        # -----------------------------------------------------

        session = self._update(
            session,
            state=AuthenticationState.QR_SCANNED,
            method=AuthenticationMethod.QR,
            student_id=student_id,
        )

        session = self._update(
            session,
            state=AuthenticationState.AUTHENTICATED,
            authenticated=True,
            unknown=False,
        )

        return AuthenticationResult(
            accepted=True,
            state=AuthenticationState.AUTHENTICATED,
            authenticated=True,
            unknown=False,
            student_id=student_id,
            method=AuthenticationMethod.QR,
            confidence=None,
            message="Student authenticated successfully using QR.",
            updated_at=session.updated_at,
        )

    # =========================================================
    # EXPLICIT ENTRY / EXIT
    # =========================================================

    def perform_lab_action(
        self,
        session_id: str,
        action: LabAction,
        db: Session,
    ) -> AuthenticationActionResult:

        session = self.get_session(session_id)

        # -----------------------------------------------------
        # SESSION VALIDATION
        # -----------------------------------------------------

        if session is None:

            raise HTTPException(
                status_code=404,
                detail="Authentication session not found.",
            )

        # -----------------------------------------------------
        # AUTHENTICATION VALIDATION
        # -----------------------------------------------------

        if not session.authenticated:

            if session.unknown:

                raise HTTPException(
                    status_code=403,
                    detail=(
                        "Unknown person. "
                        "Authentication required before lab access."
                    ),
                )

            raise HTTPException(
                status_code=403,
                detail=(
                    "Student is not authenticated. "
                    "Lab access denied."
                ),
            )

        if not session.student_id:

            raise HTTPException(
                status_code=403,
                detail="Authenticated session has no student ID.",
            )

        student_id = session.student_id

        # =====================================================
        # ENTRY
        # =====================================================

        if action == LabAction.ENTRY:

            attendance = check_in(
                student_id=student_id,
                db=db,
            )

            try:

                lab_session = start_session(
                    student_id=student_id,
                    attendance_id=attendance.attendance_id,
                    db=db,
                )

            except Exception:

                # If lab session creation fails after check-in,
                # rollback the current transaction where possible.
                db.rollback()
                raise

            return AuthenticationActionResult(
                accepted=True,
                student_id=student_id,
                action=LabAction.ENTRY,
                attendance_id=str(
                    attendance.attendance_id
                ),
                lab_session_id=str(
                    lab_session.session_id
                ),
                message=(
                    "Student authenticated and entered "
                    "the lab successfully."
                ),
            )

        # =====================================================
        # EXIT
        # =====================================================

        if action == LabAction.EXIT:

            lab_session = end_session(
                student_id=student_id,
                db=db,
            )

            attendance = check_out(
                student_id=student_id,
                db=db,
            )

            # Prevent the same authentication session from
            # being reused for another lab action.
            self._update(
                session,
                authenticated=False,
                unknown=False,
                state=AuthenticationState.IDLE,
                student_id=None,
                method=AuthenticationMethod.NONE,
                confidence=None,
            )

            return AuthenticationActionResult(
                accepted=True,
                student_id=student_id,
                action=LabAction.EXIT,
                attendance_id=str(
                    attendance.attendance_id
                ),
                lab_session_id=str(
                    lab_session.session_id
                ),
                message=(
                    "Student exited the lab successfully."
                ),
            )

        raise HTTPException(
            status_code=400,
            detail="Invalid lab action. Use ENTRY or EXIT.",
        )

    # =========================================================
    # RESET
    # =========================================================

    def reset_session(
        self,
        session_id: str,
    ) -> AuthenticationResult:

        session = self.get_session(session_id)

        if session is None:

            return AuthenticationResult(
                accepted=False,
                state=AuthenticationState.REJECTED,
                authenticated=False,
                unknown=False,
                message="Authentication session not found.",
            )

        session = self._update(
            session,
            state=AuthenticationState.IDLE,
            student_id=None,
            method=AuthenticationMethod.NONE,
            confidence=None,
            authenticated=False,
            unknown=False,
        )

        return AuthenticationResult(
            accepted=True,
            state=AuthenticationState.IDLE,
            authenticated=False,
            unknown=False,
            student_id=None,
            method=AuthenticationMethod.NONE,
            confidence=None,
            message="Authentication session reset successfully.",
            updated_at=session.updated_at,
        )

    # =========================================================
    # ACTIVE SESSIONS
    # =========================================================

    def get_active_sessions(self):

        return [
            session
            for session in self.sessions.values()
            if session.state != AuthenticationState.IDLE
        ]

    # =========================================================
    # AUTHENTICATED SESSIONS
    # =========================================================

    def get_authenticated_sessions(self):

        return [
            session
            for session in self.sessions.values()
            if session.authenticated
        ]


authentication_service = AuthenticationService()