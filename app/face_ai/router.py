from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.face_ai.schemas import (
    FaceRecognitionRequest,
    FaceRegistrationRequest
)

from app.face_ai.service import (
    register_face,
    recognize_face
)

router = APIRouter(
    prefix="/face",
    tags=["Face AI"]
)


@router.post("/recognize")
def recognize(
    data: FaceRecognitionRequest,
    db: Session = Depends(get_db)
):
    return recognize_face(data, db)


@router.post("/register")
def register(
    data: FaceRegistrationRequest,
    db: Session = Depends(get_db)
):
    return register_face(data, db)