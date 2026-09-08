import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class BorrowTransaction(Base):

    __tablename__ = "borrow_transactions"

    transaction_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.student_id"),
        nullable=False
    )

    component_id = Column(
        UUID(as_uuid=True),
        ForeignKey("inventory.component_id"),
        nullable=False
    )

    quantity = Column(Integer)

    borrow_time = Column(
        DateTime(timezone=True)
    )

    return_time = Column(
        DateTime(timezone=True),
        nullable=True
    )

    status = Column(
        String(20),
        default="BORROWED"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )