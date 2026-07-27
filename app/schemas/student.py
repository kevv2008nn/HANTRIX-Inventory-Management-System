from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


class StudentCreate(BaseModel):
    register_no: str
    name: str
    department: str
    year: int
    section: str
    email: EmailStr
    phone: str
    rfid_uid: str
    status: str = "ACTIVE"
    graduation_year: Optional[int] = None


class StudentResponse(BaseModel):
    student_id: UUID
    register_no: str
    name: str
    department: str
    year: int
    section: str
    email: EmailStr
    phone: str
    rfid_uid: str
    status: str
    graduation_year: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    year: Optional[int] = None
    section: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    rfid_uid: Optional[str] = None
    status: Optional[str] = None
    graduation_year: Optional[int] = None