from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.faculty.schemas import FacultyCreate
from app.faculty.service import (
    create_faculty,
    get_all_faculty
)

router = APIRouter(
    prefix="/faculty",
    tags=["Faculty"]
)


@router.post("/")
def add_faculty(
    data: FacultyCreate,
    db: Session = Depends(get_db)
):

    return create_faculty(
        data,
        db
    )


@router.get("/")
def faculty_list(
    db: Session = Depends(get_db)
):

    return get_all_faculty(db)