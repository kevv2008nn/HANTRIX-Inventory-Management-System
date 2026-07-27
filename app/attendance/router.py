from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.attendance.schemas import AttendanceEntry
from app.attendance.schemas import AttendanceExit

from app.attendance.service import (
    check_in,
    check_out,
    attendance_history,
    students_inside
)

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post("/checkin")
def student_checkin(
    data: AttendanceEntry,
    db: Session = Depends(get_db)
):

    return check_in(
        data.student_id,
        db
    )


@router.post("/checkout")
def student_checkout(
    data: AttendanceExit,
    db: Session = Depends(get_db)
):

    return check_out(
        data.student_id,
        db
    )


@router.get("/history/{student_id}")
def history(
    student_id: UUID,
    db: Session = Depends(get_db)
):

    return attendance_history(
        student_id,
        db
    )


@router.get("/inside")
def inside(
    db: Session = Depends(get_db)
):

    return students_inside(db)