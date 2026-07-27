from uuid import UUID

from pydantic import BaseModel


class StudentProfileCreate(BaseModel):

    student_id: UUID


class StudentProfileResponse(BaseModel):

    student_id: UUID

    total_lab_hours: float

    total_visits: int

    total_components_borrowed: int

    completed_projects: int

    hackathons: int

    certifications: int

    ai_score: float

    placement_score: float

    status: str

    class Config:

        from_attributes = True