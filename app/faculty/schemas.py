from pydantic import BaseModel, EmailStr


class FacultyCreate(BaseModel):

    employee_id: str
    name: str
    department: str
    designation: str
    email: EmailStr
    phone: str


class FacultyResponse(BaseModel):

    employee_id: str
    name: str
    department: str
    designation: str
    email: EmailStr
    phone: str
    role: str
    status: str

    class Config:
        from_attributes = True