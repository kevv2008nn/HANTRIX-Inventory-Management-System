from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AttendanceEntry(BaseModel):

    student_id: str


class AttendanceExit(BaseModel):

    student_id: str


class AttendanceAction(BaseModel):

    student_id: str

    action: str
    # ENTRY or EXIT


class AttendanceResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    attendance_id: UUID

    student_id: str

    attendance_date: date

    entry_time: datetime

    exit_time: datetime | None

    status: str