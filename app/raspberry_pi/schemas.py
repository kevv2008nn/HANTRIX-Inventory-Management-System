from pydantic import BaseModel


class RFIDScan(BaseModel):
    rfid_uid: str


class QRScan(BaseModel):
    qr_code: str


class SensorData(BaseModel):
    device_id: str
    temperature: float
    humidity: float