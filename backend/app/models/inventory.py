import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    # --------------------------------------------------------
    # PRIMARY KEY
    # --------------------------------------------------------

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # --------------------------------------------------------
    # COMPONENT ID
    # Example: ESP32-001
    # --------------------------------------------------------

    component_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    component_name = Column(
        String(255),
        nullable=False,
    )

    # --------------------------------------------------------
    # COMPONENT INFORMATION
    # --------------------------------------------------------

    category = Column(
        String(100),
        nullable=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    rack = Column(
        String(100),
        nullable=True,
    )

    shelf = Column(
        String(100),
        nullable=True,
    )

    location_code = Column(
        String(150),
        nullable=True,
    )

    # --------------------------------------------------------
    # STOCK
    # --------------------------------------------------------

    quantity = Column(
        Integer,
        nullable=False,
        default=0,
    )

    minimum_quantity = Column(
        Integer,
        nullable=False,
        default=0,
    )

    # --------------------------------------------------------
    # IDENTIFICATION
    # --------------------------------------------------------

    qr_code = Column(
        String(255),
        unique=True,
        nullable=True,
    )

    rfid_tag = Column(
        String(255),
        unique=True,
        nullable=True,
    )

    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    condition = Column(
        String(50),
        nullable=True,
        default="GOOD",
    )

    status = Column(
        String(50),
        nullable=True,
        default="AVAILABLE",
    )

    # --------------------------------------------------------
    # AI
    # --------------------------------------------------------

    image_path = Column(
        Text,
        nullable=True,
    )

    detection_label = Column(
        String(150),
        nullable=True,
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )