from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.analytics.service import dashboard_stats

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/dashboard")
def analytics_dashboard(
    db: Session = Depends(get_db)
):

    return dashboard_stats(db)