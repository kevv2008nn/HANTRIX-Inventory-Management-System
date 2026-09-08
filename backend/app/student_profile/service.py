from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.student_profile.models import StudentProfile


def create_profile(student_id, db: Session):

    existing = db.query(StudentProfile).filter(
        StudentProfile.student_id == student_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists"
        )

    profile = StudentProfile(
        student_id=student_id
    )

    db.add(profile)

    db.commit()

    db.refresh(profile)

    return profile


def get_profile(student_id, db: Session):

    profile = db.query(StudentProfile).filter(
        StudentProfile.student_id == student_id
    ).first()

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile