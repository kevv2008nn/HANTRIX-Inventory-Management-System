import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class LabSession(Base):

    __tablename__ = "lab_sessions"

    session_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.student_id"),
        nullable=False
    )

    attendance_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attendance.attendance_id"),
        nullable=False
    )

    start_time = Column(
        DateTime(timezone=True),
        nullable=False
    )

    end_time = Column(
        DateTime(timezone=True),
        nullable=True
    )

    duration = Column(
        String(30),
        default="0 Minutes"
    )

    status = Column(
        String(20),
        default="ACTIVE"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )