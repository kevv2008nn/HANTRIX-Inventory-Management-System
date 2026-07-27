from datetime import datetime
from datetime import date
from uuid import UUID

from pydantic import BaseModel


class AttendanceEntry(BaseModel):

    student_id: UUID


class AttendanceExit(BaseModel):

    student_id: UUID


class AttendanceResponse(BaseModel):

    attendance_id: UUID

    student_id: UUID

    attendance_date: date

    entry_time: datetime

    exit_time: datetime | None

    status: str

    class Config:

        from_attributes = True