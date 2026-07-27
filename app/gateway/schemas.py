from pydantic import BaseModel
from typing import Optional


class GatewayEvent(BaseModel):
    event_type: str

    student_id: Optional[str] = None

    qr_code: Optional[str] = None

    camera_id: Optional[str] = None

    temperature: Optional[float] = None

    humidity: Optional[float] = None

    confidence: Optional[float] = None