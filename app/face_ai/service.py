from sqlalchemy.orm import Session

from app.notifications.models import Notification

from app.face_ai.register import register_face as register
from app.face_ai.recognize import recognize_face as recognize

from app.attendance.service import check_in
from app.lab_sessions.service import start_session


def register_face(data, db: Session):

    status = register(
        data.student_id,
        data.image_path
    )

    if status:

        notification = Notification(
            title="Face Registered",
            message=f"Face registered for {data.student_id}",
            receiver="ADMIN",
            type="FACE_AI"
        )

        db.add(notification)
        db.commit()

    return {
        "registered": status,
        "student_id": data.student_id
    }


def recognize_student(data, db: Session):

    result = recognize(
        data.image_path
    )

    if result is None:

        notification = Notification(
            title="Unknown Face",
            message="Unknown person detected.",
            receiver="ADMIN",
            type="FACE_AI"
        )

        db.add(notification)
        db.commit()

        return {
            "recognized": False,
            "student_id": None,
            "confidence": 0
        }

    student_id = result["student_id"]
    confidence = result["confidence"]

    try:

        attendance = check_in(
            student_id,
            db
        )

        start_session(
            student_id,
            attendance.attendance_id,
            db
        )

    except Exception:
        pass

    notification = Notification(
        title="Face Recognition",
        message=f"{student_id} entered the lab.",
        receiver="ADMIN",
        type="FACE_AI"
    )

    db.add(notification)
    db.commit()

    return {
        "recognized": True,
        "student_id": student_id,
        "confidence": confidence
    }