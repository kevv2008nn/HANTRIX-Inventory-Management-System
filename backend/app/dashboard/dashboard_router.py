from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.models.student import Student
from app.models.inventory import Inventory

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(db: Session = Depends(get_db)):

    total_students = db.query(func.count(Student.student_id)).scalar() or 0

    total_inventory = db.query(func.count(Inventory.component_id)).scalar() or 0

    available_items = (
        db.query(func.count(Inventory.component_id))
        .filter(Inventory.status == "Available")
        .scalar()
        or 0
    )

    low_stock = (
        db.query(func.count(Inventory.component_id))
        .filter(Inventory.quantity <= Inventory.minimum_quantity)
        .scalar()
        or 0
    )

    return {
        "students": total_students,
        "inventory": total_inventory,
        "available_components": available_items,
        "low_stock": low_stock,
        "borrowed_components": total_inventory - available_items
    }