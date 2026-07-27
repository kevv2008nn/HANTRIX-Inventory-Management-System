from uuid import UUID
from pydantic import BaseModel


class StartSession(BaseModel):
    student_id: UUID
    attendance_id: UUID


class EndSession(BaseModel):
    student_id: UUID


class SessionResponse(BaseModel):
    session_id: UUID
    student_id: UUID
    attendance_id: UUID
    duration: str
    status: str

    class Config:
        from_attributes = True