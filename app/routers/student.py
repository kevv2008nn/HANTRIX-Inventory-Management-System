from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):

    existing = db.query(Student).filter(
        Student.register_no == student.register_no
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Register Number already exists"
        )

    new_student = Student(
        register_no=student.register_no,
        name=student.name,
        department=student.department,
        year=student.year,
        section=student.section,
        email=student.email,
        phone=student.phone,
        rfid_uid=student.rfid_uid,
        status=student.status,
        graduation_year=student.graduation_year
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):

    student = db.query(Student).filter(
        Student.student_id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: str,
    updated: StudentUpdate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.student_id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    data = updated.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student


@router.delete("/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):

    student = db.query(Student).filter(
        Student.student_id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }