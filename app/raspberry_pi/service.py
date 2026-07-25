from sqlalchemy.orm import Session

from app.notifications.models import Notification


def rfid_scan(data, db: Session):

    notification = Notification(
        title="RFID Scan",
        message=f"RFID {data.rfid_uid} scanned.",
        receiver="SYSTEM",
        type="RFID"
    )

    db.add(notification)
    db.commit()

    return {
        "status": "RFID Received"
    }


def qr_scan(data, db: Session):

    notification = Notification(
        title="QR Scan",
        message=f"QR {data.qr_code} scanned.",
        receiver="SYSTEM",
        type="QR"
    )

    db.add(notification)
    db.commit()

    return {
        "status": "QR Received"
    }


def sensor_update(data, db: Session):

    notification = Notification(
        title="Sensor Update",
        message=f"T={data.temperature} H={data.humidity}",
        receiver="SYSTEM",
        type="SENSOR"
    )

    db.add(notification)
    db.commit()

    return {
        "status": "Sensor Data Received"
    }