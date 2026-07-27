import uuid

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class Student(Base):

    __tablename__ = "students"

    student_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    register_no = Column(
        String(20),
        unique=True,
        nullable=False
    )

    name = Column(
        String(100),
        nullable=False
    )

    department = Column(
        String(50),
        nullable=False
    )

    year = Column(
        Integer,
        nullable=False
    )

    section = Column(
        String(10),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True
    )

    phone = Column(
        String(20)
    )

    rfid_uid = Column(
        String(100),
        unique=True
    )

    photo = Column(
        String
    )

    status = Column(
        String(20),
        default="ACTIVE"
    )

    joined_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    graduation_year = Column(
        Integer
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )