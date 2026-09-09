from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.lab_sessions.models import LabSession


def utc_now():
    return datetime.now(timezone.utc)


def calculate_duration(
    start_time: datetime,
    end_time: datetime,
) -> str:

    seconds = int(
        (end_time - start_time).total_seconds()
    )

    if seconds < 0:
        seconds = 0

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:

        return (
            f"{hours} Hour(s) "
            f"{minutes} Minute(s)"
        )

    if minutes > 0:

        return (
            f"{minutes} Minute(s) "
            f"{remaining_seconds} Second(s)"
        )

    return f"{remaining_seconds} Second(s)"


# ============================================================
# FIND ACTIVE SESSION
# ============================================================

def get_active_session(
    student_id: str,
    db: Session,
) -> Optional[LabSession]:

    return (
        db.query(LabSession)
        .filter(
            LabSession.student_id == student_id,
            LabSession.status == "ACTIVE",
            LabSession.end_time.is_(None),
        )
        .order_by(
            LabSession.start_time.desc()
        )
        .first()
    )


# ============================================================
# START SESSION
# ============================================================

def start_session(
    student_id: str,
    attendance_id,
    db: Session,
):

    existing = get_active_session(
        student_id=student_id,
        db=db,
    )

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Student already has an active lab session.",
        )

    session = LabSession(
        student_id=student_id,
        attendance_id=attendance_id,
        start_time=utc_now(),
        status="ACTIVE",
        duration="0 Minutes",
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    return session


# ============================================================
# END SESSION
# ============================================================

def end_session(
    student_id: str,
    db: Session,
):

    session = get_active_session(
        student_id=student_id,
        db=db,
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="No active lab session found.",
        )

    end_time = utc_now()

    session.end_time = end_time

    session.duration = calculate_duration(
        start_time=session.start_time,
        end_time=end_time,
    )

    session.status = "COMPLETED"

    db.commit()

    db.refresh(session)

    return session


# ============================================================
# GET SESSION
# ============================================================

def get_session(
    session_id,
    db: Session,
):

    session = (
        db.query(LabSession)
        .filter(
            LabSession.session_id == session_id
        )
        .first()
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Lab session not found.",
        )

    return session


# ============================================================
# STUDENT SESSION HISTORY
# ============================================================

def get_student_sessions(
    student_id: str,
    db: Session,
):

    return (
        db.query(LabSession)
        .filter(
            LabSession.student_id == student_id
        )
        .order_by(
            LabSession.start_time.desc()
        )
        .all()
    )


# ============================================================
# ACTIVE STUDENTS
# ============================================================

def get_active_sessions(
    db: Session,
):

    return (
        db.query(LabSession)
        .filter(
            LabSession.status == "ACTIVE",
            LabSession.end_time.is_(None),
        )
        .order_by(
            LabSession.start_time.desc()
        )
        .all()
    )