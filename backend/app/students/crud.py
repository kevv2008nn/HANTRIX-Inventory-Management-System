from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.students.model import Student


def create_student(db: Session, student):

    if get_student(db, student.student_id):
        raise HTTPException(status_code=409, detail="Student ID already exists")

    db_student = Student(**student.model_dump())

    db.add(db_student)

    db.commit()

    db.refresh(db_student)

    return db_student


def get_students(db: Session):

    return db.query(Student).all()


def get_student(db: Session, student_id: str):

    return db.query(Student).filter(
        Student.student_id == student_id
    ).first()


def delete_student(db: Session, student_id: str):

    student = get_student(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return student