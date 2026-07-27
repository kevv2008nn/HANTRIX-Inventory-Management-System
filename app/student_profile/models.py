import uuid

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base


class StudentProfile(Base):

    __tablename__ = "student_profiles"

    profile_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.student_id"),
        unique=True
    )

    total_lab_hours = Column(
        Float,
        default=0
    )

    total_visits = Column(
        Integer,
        default=0
    )

    total_components_borrowed = Column(
        Integer,
        default=0
    )

    completed_projects = Column(
        Integer,
        default=0
    )

    hackathons = Column(
        Integer,
        default=0
    )

    certifications = Column(
        Integer,
        default=0
    )

    ai_score = Column(
        Float,
        default=0
    )

    placement_score = Column(
        Float,
        default=0
    )

    status = Column(
        String(20),
        default="ACTIVE"
    )