from datetime import datetime, date, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.attendance.models import Attendance
from app.student_profile.models import StudentProfile
from app.notifications.models import Notification


def utc_now():
    return datetime.now(timezone.utc)


# ============================================================
# CHECK IN
# ============================================================

def check_in(
    student_id: str,
    db: Session
):

    # --------------------------------------------------------
    # Check whether student already has an active attendance
    # --------------------------------------------------------

    existing = (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student_id,
            Attendance.exit_time.is_(None),
            Attendance.status == "IN"
        )
        .first()
    )

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Student already inside lab."
        )

    # --------------------------------------------------------
    # Create attendance
    # --------------------------------------------------------

    attendance = Attendance(
        student_id=student_id,
        attendance_date=date.today(),
        entry_time=utc_now(),
        status="IN"
    )

    db.add(attendance)
    db.flush()

    # --------------------------------------------------------
    # Update student lifetime visits
    # --------------------------------------------------------

    profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.student_id == student_id
        )
        .first()
    )

    if profile:

        profile.total_visits = (
            profile.total_visits or 0
        ) + 1

    # --------------------------------------------------------
    # Notification
    # --------------------------------------------------------

    notification = Notification(
        title="Student Checked In",
        message=f"Student {student_id} entered the lab.",
        receiver="ADMIN",
        type="ATTENDANCE"
    )

    db.add(notification)

    db.commit()
    db.refresh(attendance)

    return attendance


# ============================================================
# CHECK OUT
# ============================================================

def check_out(
    student_id: str,
    db: Session
):

    # --------------------------------------------------------
    # IMPORTANT:
    # This happens ONLY when the student explicitly chooses
    # EXIT after authentication.
    #
    # Camera disappearance NEVER calls this automatically.
    # --------------------------------------------------------

    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student_id,
            Attendance.exit_time.is_(None),
            Attendance.status == "IN"
        )
        .order_by(
            Attendance.entry_time.desc()
        )
        .first()
    )

    if attendance is None:

        raise HTTPException(
            status_code=404,
            detail="No active attendance found."
        )

    # --------------------------------------------------------
    # Close attendance
    # --------------------------------------------------------

    attendance.exit_time = utc_now()
    attendance.status = "OUT"

    # --------------------------------------------------------
    # Notification
    # --------------------------------------------------------

    notification = Notification(
        title="Student Checked Out",
        message=f"Student {student_id} exited the lab.",
        receiver="ADMIN",
        type="ATTENDANCE"
    )

    db.add(notification)

    db.commit()
    db.refresh(attendance)

    return attendance


# ============================================================
# ENTRY / EXIT ACTION
# ============================================================

def process_attendance_action(
    student_id: str,
    action: str,
    db: Session
):

    action = action.strip().upper()

    if action == "ENTRY":

        return check_in(
            student_id=student_id,
            db=db
        )

    if action == "EXIT":

        return check_out(
            student_id=student_id,
            db=db
        )

    raise HTTPException(
        status_code=400,
        detail="Invalid action. Use ENTRY or EXIT."
    )


# ============================================================
# ATTENDANCE HISTORY
# ============================================================

def attendance_history(
    student_id: str,
    db: Session
):

    return (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student_id
        )
        .order_by(
            Attendance.entry_time.desc()
        )
        .all()
    )


# ============================================================
# STUDENTS CURRENTLY INSIDE
# ============================================================

def students_inside(
    db: Session
):

    return (
        db.query(Attendance)
        .filter(
            Attendance.exit_time.is_(None),
            Attendance.status == "IN"
        )
        .order_by(
            Attendance.entry_time.desc()
        )
        .all()
    )


# ============================================================
# CURRENT ATTENDANCE
# ============================================================

def current_attendance(
    student_id: str,
    db: Session
):

    return (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student_id,
            Attendance.exit_time.is_(None),
            Attendance.status == "IN"
        )
        .order_by(
            Attendance.entry_time.desc()
        )
        .first()
    )