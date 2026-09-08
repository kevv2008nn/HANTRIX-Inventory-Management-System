from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.lab_sessions.models import LabSession
from app.student_profile.models import StudentProfile
from app.attendance.models import Attendance
from app.notifications.models import Notification


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


def enter_lab(student_id, db: Session):

    # Check if student already has an active lab session
    existing_session = db.query(LabSession).filter(
        LabSession.student_id == student_id,
        LabSession.status == "ACTIVE"
    ).first()

    if existing_session:
        raise HTTPException(
            status_code=400,
            detail="Student is already inside the lab."
        )

    # Create attendance
    attendance = Attendance(
        student_id=student_id,
        attendance_date=datetime.now().date(),
        entry_time=datetime.now(),
        status="IN"
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    # Create lab session
    session = LabSession(
        student_id=student_id,
        attendance_id=attendance.attendance_id,
        start_time=datetime.now(),
        status="ACTIVE"
    )

    db.add(session)

    # Update student profile
    profile = db.query(StudentProfile).filter(
        StudentProfile.student_id == student_id
    ).first()

    if profile:
        profile.total_visits += 1

    # Notification
    notification = Notification(
        title="Student Entered Lab",
        message=f"Student {student_id} entered the lab.",
        receiver="ADMIN",
        type="ATTENDANCE"
    )

    db.add(notification)

    db.commit()
    db.refresh(session)

    return {
        "success": True,
        "message": "Student entered lab successfully",
        "student_id": student_id,
        "attendance_id": attendance.attendance_id,
        "session_id": session.session_id,
        "entry_time": session.start_time,
        "status": session.status
    }


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

    session.duration = f"{round(hours, 2)} Hours"
    session.status = "COMPLETED"

    # Close attendance
    attendance = db.query(Attendance).filter(
        Attendance.attendance_id == session.attendance_id
    ).first()

    if attendance:
        attendance.exit_time = session.end_time
        attendance.status = "OUT"

    # Update total lab hours
    profile = db.query(StudentProfile).filter(
        StudentProfile.student_id == student_id
    ).first()

    if profile:
        profile.total_lab_hours += hours

    # Notification
    notification = Notification(
        title="Student Exited Lab",
        message=f"Student {student_id} left the lab.",
        receiver="ADMIN",
        type="ATTENDANCE"
    )

    db.add(notification)

    db.commit()
    db.refresh(session)

    return session


def active_sessions(db: Session):

    return db.query(LabSession).filter(
        LabSession.status == "ACTIVE"
    ).all()