from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.students.schemas import StudentCreate
from app.students.service import *

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/")
def add(
    data: StudentCreate,
    db: Session = Depends(get_db)
):
    return add_student(data, db)


@router.get("/")
def all(
    db: Session = Depends(get_db)
):
    return all_students(db)


@router.get("/{student_id}")
def one(
    student_id: str,
    db: Session = Depends(get_db)
):
    return one_student(student_id, db)


@router.delete("/{student_id}")
def delete(
    student_id: str,
    db: Session = Depends(get_db)
):
    return remove_student(student_id, db)