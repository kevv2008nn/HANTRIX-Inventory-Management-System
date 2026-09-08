from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class InventoryBase(BaseModel):

    component_id: str
    component_name: str

    category: Optional[str] = None
    description: Optional[str] = None

    rack: Optional[str] = None
    shelf: Optional[str] = None
    location_code: Optional[str] = None

    quantity: int = 0
    minimum_quantity: int = 0

    qr_code: Optional[str] = None
    rfid_tag: Optional[str] = None

    condition: str = "GOOD"
    status: str = "AVAILABLE"

    image_path: Optional[str] = None
    detection_label: Optional[str] = None


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):

    component_name: Optional[str] = None

    category: Optional[str] = None
    description: Optional[str] = None

    rack: Optional[str] = None
    shelf: Optional[str] = None
    location_code: Optional[str] = None

    quantity: Optional[int] = None
    minimum_quantity: Optional[int] = None

    qr_code: Optional[str] = None
    rfid_tag: Optional[str] = None

    condition: Optional[str] = None
    status: Optional[str] = None

    image_path: Optional[str] = None
    detection_label: Optional[str] = None


class InventoryResponse(InventoryBase):

    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None