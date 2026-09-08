import uuid

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from app.database.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    alert_type = Column(
        String(100),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    severity = Column(
        String(30),
        nullable=False
    )

    student_id = Column(
        String(100),
        nullable=True
    )

    component_id = Column(
        String(100),
        nullable=True
    )

    camera_id = Column(
        String(100),
        nullable=True
    )

    transaction_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )

    status = Column(
        String(30),
        nullable=False,
        default="OPEN"
    )

    # IMPORTANT:
    # "metadata" is reserved by SQLAlchemy.
    # Python attribute = event_metadata
    # PostgreSQL column = metadata
    event_metadata = Column(
        "metadata",
        JSONB,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    resolved_at = Column(
        DateTime(timezone=True),
        nullable=True
    )