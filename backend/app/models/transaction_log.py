import uuid

from sqlalchemy import Column, String, Text, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.database import Base


class TransactionLog(Base):
    __tablename__ = "transaction_logs"

    log_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    transaction_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    student_id = Column(
        String(100),
        nullable=False
    )

    component_id = Column(
        String(100),
        nullable=False
    )

    event_type = Column(
        String(50),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    camera_id = Column(
        String(100),
        nullable=True
    )

    confidence = Column(
        Float,
        nullable=True
    )

    # IMPORTANT:
    # "metadata" is reserved by SQLAlchemy.
    # Therefore the Python attribute is event_metadata.
    event_metadata = Column(
        "metadata",
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )