from sqlalchemy.orm import Session

from app.notifications.models import Notification


def create_notification(data, db: Session):

    notification = Notification(**data.model_dump())

    db.add(notification)

    db.commit()

    db.refresh(notification)

    return notification


def get_notifications(db: Session):

    return db.query(Notification).order_by(
        Notification.created_at.desc()
    ).all()