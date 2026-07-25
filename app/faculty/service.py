from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.faculty.models import Faculty


def create_faculty(data, db: Session):

    existing = db.query(Faculty).filter(
        Faculty.employee_id == data.employee_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Faculty Already Exists"
        )

    faculty = Faculty(**data.model_dump())

    db.add(faculty)
    db.commit()
    db.refresh(faculty)

    return faculty


def get_all_faculty(db: Session):

    return db.query(Faculty).all()