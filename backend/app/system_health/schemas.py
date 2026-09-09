from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HealthCheck(BaseModel):
    name: str
    status: str
    message: str
    response_time_ms: Optional[float] = None
    checked_at: datetime


class SystemHealthResponse(BaseModel):
    status: str
    service: str
    version: str
    checked_at: datetime
    checks: list[HealthCheck]


class DatabaseHealthResponse(BaseModel):
    status: str
    database: str
    connected: bool
    message: str
    response_time_ms: Optional[float] = None
    checked_at: datetime


class AIHealthResponse(BaseModel):
    status: str
    face_recognition: str
    event_engine: str
    message: str
    checked_at: datetime


class CameraHealthResponse(BaseModel):
    status: str
    camera_1: str
    camera_2: str
    message: str
    checked_at: datetime