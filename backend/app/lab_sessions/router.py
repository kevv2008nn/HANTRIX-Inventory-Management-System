from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.lab_sessions.schemas import (
    LabSessionStart,
    LabSessionEnd,
    LabSessionResponse,
)

from app.lab_sessions.service import (
    start_session,
    end_session,
    get_session,
    get_student_sessions,
    get_active_session,
    get_active_sessions,
)


router = APIRouter(
    prefix="/lab-sessions",
    tags=["Lab Sessions"],
)


# ============================================================
# START
# ============================================================

@router.post(
    "/start",
    response_model=LabSessionResponse,
)
def start_lab_session(
    data: LabSessionStart,
    db: Session = Depends(get_db),
):

    return start_session(
        student_id=data.student_id,
        attendance_id=data.attendance_id,
        db=db,
    )


# ============================================================
# END
# ============================================================

@router.post(
    "/end",
    response_model=LabSessionResponse,
)
def end_lab_session(
    data: LabSessionEnd,
    db: Session = Depends(get_db),
):

    return end_session(
        student_id=data.student_id,
        db=db,
    )


# ============================================================
# CURRENT ACTIVE SESSION
# ============================================================

@router.get(
    "/active/{student_id}",
)
def active_student_session(
    student_id: str,
    db: Session = Depends(get_db),
):

    session = get_active_session(
        student_id=student_id,
        db=db,
    )

    if session is None:

        return {
            "active": False,
            "session": None,
        }

    return {
        "active": True,
        "session": session,
    }


# ============================================================
# SESSION BY ID
# ============================================================

@router.get(
    "/{session_id}",
    response_model=LabSessionResponse,
)
def session_by_id(
    session_id,
    db: Session = Depends(get_db),
):

    return get_session(
        session_id=session_id,
        db=db,
    )


# ============================================================
# STUDENT HISTORY
# ============================================================

@router.get(
    "/student/{student_id}",
)
def student_session_history(
    student_id: str,
    db: Session = Depends(get_db),
):

    sessions = get_student_sessions(
        student_id=student_id,
        db=db,
    )

    return {
        "count": len(sessions),
        "sessions": sessions,
    }


# ============================================================
# ALL ACTIVE SESSIONS
# ============================================================

@router.get(
    "/runtime/active",
)
def all_active_sessions(
    db: Session = Depends(get_db),
):

    sessions = get_active_sessions(
        db=db,
    )

    return {
        "count": len(sessions),
        "sessions": sessions,
    }