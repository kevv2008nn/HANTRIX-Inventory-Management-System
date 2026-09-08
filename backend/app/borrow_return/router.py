from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.borrow_return.schemas import (
    BorrowItem,
    ReturnItem
)

from app.borrow_return.service import (
    borrow_component,
    return_component,
    student_borrowed_components
)


router = APIRouter(
    prefix="/borrow",
    tags=["Borrow & Return"]
)


@router.post("/borrow")
def borrow(
    data: BorrowItem,
    db: Session = Depends(get_db)
):

    return borrow_component(
        data,
        db
    )


@router.post("/return")
def return_item(
    data: ReturnItem,
    db: Session = Depends(get_db)
):

    return return_component(
        data,
        db
    )


@router.get("/student/{student_id}")
def student_components(
    student_id: UUID,
    db: Session = Depends(get_db)
):

    return student_borrowed_components(
        student_id,
        db
    )