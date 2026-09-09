from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.attendance.schemas import (
    AttendanceEntry,
    AttendanceExit,
    AttendanceAction,
)

from app.attendance.service import (
    check_in,
    check_out,
    process_attendance_action,
    attendance_history,
    students_inside,
    current_attendance,
)


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


# ============================================================
# ENTRY
# ============================================================

@router.post("/checkin")
def student_checkin(
    data: AttendanceEntry,
    db: Session = Depends(get_db)
):

    return check_in(
        student_id=data.student_id,
        db=db
    )


# ============================================================
# EXIT
# ============================================================

@router.post("/checkout")
def student_checkout(
    data: AttendanceExit,
    db: Session = Depends(get_db)
):

    return check_out(
        student_id=data.student_id,
        db=db
    )


# ============================================================
# EXPLICIT ENTRY / EXIT ACTION
# ============================================================

@router.post("/action")
def attendance_action(
    data: AttendanceAction,
    db: Session = Depends(get_db)
):

    return process_attendance_action(
        student_id=data.student_id,
        action=data.action,
        db=db
    )


# ============================================================
# HISTORY
# ============================================================

@router.get("/history/{student_id}")
def history(
    student_id: str,
    db: Session = Depends(get_db)
):

    return attendance_history(
        student_id=student_id,
        db=db
    )


# ============================================================
# STUDENTS INSIDE
# ============================================================

@router.get("/inside")
def inside(
    db: Session = Depends(get_db)
):

    return students_inside(
        db=db
    )


# ============================================================
# CURRENT ATTENDANCE
# ============================================================

@router.get("/current/{student_id}")
def current(
    student_id: str,
    db: Session = Depends(get_db)
):

    attendance = current_attendance(
        student_id=student_id,
        db=db
    )

    if attendance is None:

        return {
            "active": False,
            "attendance": None
        }

    return {
        "active": True,
        "attendance": attendance
    }