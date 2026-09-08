import uuid

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class Inventory(Base):

    __tablename__ = "inventory"

    component_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    component_name = Column(
        String(100),
        nullable=False
    )

    category = Column(
        String(50),
        nullable=False
    )

    rack = Column(
        String(20)
    )

    shelf = Column(
        String(20)
    )

    quantity = Column(
        Integer,
        default=0
    )

    minimum_quantity = Column(
        Integer,
        default=1
    )

    qr_code = Column(
        String(100),
        unique=True
    )

    rfid_tag = Column(
        String(100),
        unique=True
    )

    condition = Column(
        String(50),
        default="Excellent"
    )

    status = Column(
        String(30),
        default="Available"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )