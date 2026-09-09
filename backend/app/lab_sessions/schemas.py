from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LabSessionStart(BaseModel):

    student_id: str

    attendance_id: UUID


class LabSessionEnd(BaseModel):

    student_id: str


class LabSessionResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    session_id: UUID

    student_id: str

    attendance_id: UUID

    start_time: datetime

    end_time: datetime | None

    duration: str | None

    status: str