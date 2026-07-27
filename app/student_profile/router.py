from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.student_profile.schemas import StudentProfileCreate
from app.student_profile.service import (
    create_profile,
    get_profile
)
from app.student_profile.models import StudentProfile

router = APIRouter(
    prefix="/profile",
    tags=["Student Profile"]
)


@router.post("/create")
def create(
    data: StudentProfileCreate,
    db: Session = Depends(get_db)
):
    return create_profile(
        data.student_id,
        db
    )


@router.get("/{student_id}")
def profile(
    student_id: UUID,
    db: Session = Depends(get_db)
):
    return get_profile(
        student_id,
        db
    )


@router.put("/graduate/{student_id}")
def graduate(
    student_id: UUID,
    db: Session = Depends(get_db)
):

    profile = db.query(StudentProfile).filter(
        StudentProfile.student_id == student_id
    ).first()

    if profile is None:
        return {
            "message": "Profile Not Found"
        }

    profile.status = "ALUMNI"

    db.commit()

    return {
        "message": "Student Graduated Successfully"
    }