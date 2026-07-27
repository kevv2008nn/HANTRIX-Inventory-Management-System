import uuid

from sqlalchemy import Column, Date, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class Attendance(Base):

    __tablename__ = "attendance"

    attendance_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.student_id"),
        nullable=False
    )

    attendance_date = Column(
        Date,
        nullable=False
    )

    entry_time = Column(
        DateTime(timezone=True),
        nullable=False
    )

    exit_time = Column(
        DateTime(timezone=True),
        nullable=True
    )

    status = Column(
        String(20),
        default="IN"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )