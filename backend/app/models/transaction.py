import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.database import Base


class Transaction(Base):

    __tablename__ = "transactions"

    transaction_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    student_id = Column(
        String(100),
        nullable=False,
        index=True,
    )

    component_id = Column(
        String(100),
        nullable=False,
        index=True,
    )

    action = Column(
        String(20),
        nullable=False,
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1,
    )

    requested_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    borrowed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    returned_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    status = Column(
        String(50),
        nullable=False,
        default="PENDING",
    )

    verification_status = Column(
        String(50),
        nullable=False,
        default="PENDING",
    )

    expected_rack = Column(
        String(100),
        nullable=True,
    )

    expected_shelf = Column(
        String(100),
        nullable=True,
    )

    camera_id = Column(
        String(100),
        nullable=True,
    )

    confidence = Column(
        Float,
        nullable=True,
    )

    mismatch_reason = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )