from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.analytics.schemas import (
    AlertAnalytics,
    AnalyticsDashboardResponse,
    AttendanceAnalytics,
    DailyVisitAnalytics,
    InventoryAnalytics,
    SessionAnalytics,
    StudentAnalytics,
    TransactionAnalytics,
)

from app.analytics.service import (
    get_alert_analytics,
    get_attendance_analytics,
    get_dashboard_analytics,
    get_daily_attendance,
    get_inventory_analytics,
    get_session_analytics,
    get_student_analytics,
    get_transaction_analytics,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


# ============================================================
# COMPLETE DASHBOARD ANALYTICS
# ============================================================

@router.get(
    "/overview",
    response_model=AnalyticsDashboardResponse,
)
def analytics_overview(
    db: Session = Depends(get_db),
):
    return get_dashboard_analytics(
        db=db
    )


# ============================================================
# ATTENDANCE
# ============================================================

@router.get(
    "/attendance",
    response_model=AttendanceAnalytics,
)
def analytics_attendance(
    db: Session = Depends(get_db),
):
    return get_attendance_analytics(
        db=db
    )


# ============================================================
# DAILY ATTENDANCE
# ============================================================

@router.get(
    "/attendance/daily",
    response_model=list[DailyVisitAnalytics],
)
def analytics_daily_attendance(
    db: Session = Depends(get_db),
):
    return get_daily_attendance(
        db=db
    )


# ============================================================
# SESSIONS
# ============================================================

@router.get(
    "/sessions",
    response_model=SessionAnalytics,
)
def analytics_sessions(
    db: Session = Depends(get_db),
):
    return get_session_analytics(
        db=db
    )


# ============================================================
# INVENTORY
# ============================================================

@router.get(
    "/inventory",
    response_model=InventoryAnalytics,
)
def analytics_inventory(
    db: Session = Depends(get_db),
):
    return get_inventory_analytics(
        db=db
    )


# ============================================================
# TRANSACTIONS
# ============================================================

@router.get(
    "/transactions",
    response_model=TransactionAnalytics,
)
def analytics_transactions(
    db: Session = Depends(get_db),
):
    return get_transaction_analytics(
        db=db
    )


# ============================================================
# ALERTS
# ============================================================

@router.get(
    "/alerts",
    response_model=AlertAnalytics,
)
def analytics_alerts(
    db: Session = Depends(get_db),
):
    return get_alert_analytics(
        db=db
    )


# ============================================================
# STUDENT ANALYTICS
# ============================================================

@router.get(
    "/students/{student_id}",
    response_model=StudentAnalytics,
)
def analytics_student(
    student_id: str,
    db: Session = Depends(get_db),
):
    return get_student_analytics(
        db=db,
        student_id=student_id,
    )