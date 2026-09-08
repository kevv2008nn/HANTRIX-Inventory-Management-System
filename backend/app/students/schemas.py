from pydantic import BaseModel


class StudentCreate(BaseModel):
    student_id: str
    name: str
    department: str
    year: int
    section: str
    email: str
    phone: str
    image_path: str


class StudentResponse(BaseModel):
    id: int
    student_id: str
    name: str
    department: str
    year: int
    section: str
    email: str
    phone: str
    image_path: str
    face_registered: bool

    class Config:
        from_attributes = True