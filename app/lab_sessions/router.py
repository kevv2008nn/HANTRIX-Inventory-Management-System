from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.lab_sessions.schemas import StartSession
from app.lab_sessions.schemas import EndSession

from app.lab_sessions.service import (
    start_session,
    end_session,
    active_sessions
)

router = APIRouter(
    prefix="/lab-session",
    tags=["Lab Session"]
)


@router.post("/start")
def session_start(
    data: StartSession,
    db: Session = Depends(get_db)
):

    return start_session(
        data.student_id,
        data.attendance_id,
        db
    )


@router.post("/end")
def session_end(
    data: EndSession,
    db: Session = Depends(get_db)
):

    return end_session(
        data.student_id,
        db
    )


@router.get("/active")
def current_sessions(
    db: Session = Depends(get_db)
):

    return active_sessions(db)