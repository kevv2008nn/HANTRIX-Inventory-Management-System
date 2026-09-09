from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.system_health.schemas import (
    AIHealthResponse,
    CameraHealthResponse,
    DatabaseHealthResponse,
    SystemHealthResponse,
)
from app.system_health.service import (
    get_ai_health,
    get_camera_health,
    get_database_health,
    get_detailed_health,
)

router = APIRouter(
    prefix="/health",
    tags=["System Health"],
)


@router.get(
    "",
    response_model=SystemHealthResponse,
)
def health_check(
    db: Session = Depends(get_db),
):
    return get_detailed_health(db)


@router.get(
    "/detailed",
    response_model=SystemHealthResponse,
)
def detailed_health_check(
    db: Session = Depends(get_db),
):
    return get_detailed_health(db)


@router.get(
    "/database",
    response_model=DatabaseHealthResponse,
)
def database_health_check(
    db: Session = Depends(get_db),
):
    return get_database_health(db)


@router.get(
    "/ai",
    response_model=AIHealthResponse,
)
def ai_health_check():
    return get_ai_health()


@router.get(
    "/cameras",
    response_model=CameraHealthResponse,
)
def camera_health_check():
    return get_camera_health()