from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.lab_sessions.models import LabSession
from app.student_profile.models import StudentProfile


def start_session(student_id, attendance_id, db: Session):

    existing = db.query(LabSession).filter(
        LabSession.student_id == student_id,
        LabSession.status == "ACTIVE"
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Session already active"
        )

    session = LabSession(
        student_id=student_id,
        attendance_id=attendance_id,
        start_time=datetime.now(),
        status="ACTIVE"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def end_session(student_id, db: Session):

    session = db.query(LabSession).filter(
        LabSession.student_id == student_id,
        LabSession.status == "ACTIVE"
    ).first()

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="No Active Session"
        )

    session.end_time = datetime.now()

    hours = (
        session.end_time - session.start_time
    ).total_seconds() / 3600

    session.duration = f"{round(hours,2)} Hours"
    session.status = "COMPLETED"

    profile = db.query(StudentProfile).filter(
        StudentProfile.student_id == student_id
    ).first()

    if profile:
        profile.total_lab_hours += hours

    db.commit()
    db.refresh(session)

    return session


def active_sessions(db: Session):

    return db.query(LabSession).filter(
        LabSession.status == "ACTIVE"
    ).all()