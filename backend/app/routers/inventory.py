from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse
)

from app.inventory.service import (
    create_inventory,
    get_all_inventory,
    get_inventory,
    update_inventory,
    delete_inventory
)


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


# ============================================================
# CREATE
# ============================================================

@router.post(
    "/",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_item(
    data: InventoryCreate,
    db: Session = Depends(get_db)
):

    existing = get_inventory(
        db,
        data.component_id
    )

    if existing:

        raise HTTPException(
            status_code=409,
            detail="Component ID already exists"
        )

    return create_inventory(
        db,
        data
    )


# ============================================================
# GET ALL
# ============================================================

@router.get(
    "/",
    response_model=list[InventoryResponse]
)
def list_inventory(
    db: Session = Depends(get_db)
):

    return get_all_inventory(db)


# ============================================================
# GET ONE
# ============================================================

@router.get(
    "/{component_id}",
    response_model=InventoryResponse
)
def get_item(
    component_id: str,
    db: Session = Depends(get_db)
):

    item = get_inventory(
        db,
        component_id
    )

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Component not found"
        )

    return item


# ============================================================
# UPDATE
# ============================================================

@router.put(
    "/{component_id}",
    response_model=InventoryResponse
)
def update_item(
    component_id: str,
    data: InventoryUpdate,
    db: Session = Depends(get_db)
):

    item = update_inventory(
        db,
        component_id,
        data
    )

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Component not found"
        )

    return item


# ============================================================
# DELETE
# ============================================================

@router.delete(
    "/{component_id}"
)
def delete_item(
    component_id: str,
    db: Session = Depends(get_db)
):

    deleted = delete_inventory(
        db,
        component_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Component not found"
        )

    return {
        "message": "Component deleted successfully",
        "component_id": component_id
    }