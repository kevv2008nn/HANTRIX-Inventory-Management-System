from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.raspberry_pi.schemas import RFIDScan
from app.raspberry_pi.schemas import QRScan
from app.raspberry_pi.schemas import SensorData

from app.raspberry_pi.service import (
    rfid_scan,
    qr_scan,
    sensor_update
)

router = APIRouter(
    prefix="/raspberry",
    tags=["Raspberry Pi"]
)


@router.post("/rfid")
def rfid(
    data: RFIDScan,
    db: Session = Depends(get_db)
):
    return rfid_scan(data, db)


@router.post("/qr")
def qr(
    data: QRScan,
    db: Session = Depends(get_db)
):
    return qr_scan(data, db)


@router.post("/sensor")
def sensor(
    data: SensorData,
    db: Session = Depends(get_db)
):
    return sensor_update(data, db)