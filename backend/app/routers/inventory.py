from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse,
    InventoryUpdate,
)

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.post("/", response_model=InventoryResponse)
def create_inventory(
    item: InventoryCreate,
    db: Session = Depends(get_db),
):

    existing = db.query(Inventory).filter(
        Inventory.qr_code == item.qr_code
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="QR Code already exists"
        )

    new_item = Inventory(
        component_name=item.component_name,
        category=item.category,
        rack=item.rack,
        shelf=item.shelf,
        quantity=item.quantity,
        minimum_quantity=item.minimum_quantity,
        qr_code=item.qr_code,
        rfid_tag=item.rfid_tag,
        condition=item.condition,
        status=item.status,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.get("/", response_model=list[InventoryResponse])
def get_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()


@router.get("/{component_id}", response_model=InventoryResponse)
def get_inventory_item(
    component_id: str,
    db: Session = Depends(get_db),
):

    item = db.query(Inventory).filter(
        Inventory.component_id == component_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Component not found"
        )

    return item


@router.put("/{component_id}", response_model=InventoryResponse)
def update_inventory(
    component_id: str,
    updated: InventoryUpdate,
    db: Session = Depends(get_db),
):

    item = db.query(Inventory).filter(
        Inventory.component_id == component_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Component not found"
        )

    data = updated.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


@router.delete("/{component_id}")
def delete_inventory(
    component_id: str,
    db: Session = Depends(get_db),
):

    item = db.query(Inventory).filter(
        Inventory.component_id == component_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Component not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Component Deleted Successfully"
    }