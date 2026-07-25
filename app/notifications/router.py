from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.notifications.schemas import NotificationCreate

from app.notifications.service import (
    create_notification,
    get_notifications
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.post("/")
def add_notification(
    data: NotificationCreate,
    db: Session = Depends(get_db)
):

    return create_notification(data, db)


@router.get("/")
def list_notifications(
    db: Session = Depends(get_db)
):

    return get_notifications(db)