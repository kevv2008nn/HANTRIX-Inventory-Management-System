from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class InventoryCreate(BaseModel):
    component_name: str
    category: str
    rack: str
    shelf: str
    quantity: int
    minimum_quantity: int
    qr_code: str
    rfid_tag: str
    condition: str
    status: str


class InventoryResponse(BaseModel):
    component_id: UUID
    component_name: str
    category: str
    rack: str
    shelf: str
    quantity: int
    minimum_quantity: int
    qr_code: str
    rfid_tag: str
    condition: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class InventoryUpdate(BaseModel):
    component_name: Optional[str] = None
    category: Optional[str] = None
    rack: Optional[str] = None
    shelf: Optional[str] = None
    quantity: Optional[int] = None
    minimum_quantity: Optional[int] = None
    qr_code: Optional[str] = None
    rfid_tag: Optional[str] = None
    condition: Optional[str] = None
    status: Optional[str] = None