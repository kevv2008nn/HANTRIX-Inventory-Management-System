import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class Faculty(Base):

    __tablename__ = "faculty"

    faculty_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    employee_id = Column(
        String(20),
        unique=True,
        nullable=False
    )

    name = Column(
        String(100),
        nullable=False
    )

    department = Column(
        String(50)
    )

    designation = Column(
        String(50)
    )

    email = Column(
        String(100),
        unique=True
    )

    phone = Column(
        String(20)
    )

    role = Column(
        String(30),
        default="FACULTY"
    )

    status = Column(
        String(20),
        default="ACTIVE"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )