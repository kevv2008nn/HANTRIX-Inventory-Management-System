from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.attendance.models import Attendance
from app.lab_sessions.models import LabSession

from app.models.inventory import Inventory
from app.models.transaction import Transaction
from app.models.alert import Alert

from app.analytics.schemas import (
    AlertAnalytics,
    AnalyticsDashboardResponse,
    AnalyticsOverview,
    AttendanceAnalytics,
    DailyVisitAnalytics,
    InventoryAnalytics,
    SessionAnalytics,
    StudentAnalytics,
    TransactionAnalytics,
)


# ============================================================
# TIME HELPERS
# ============================================================

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def make_aware(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)

    return dt


# ============================================================
# OVERDUE HELPER
# ============================================================

def get_overdue_transactions(
    db: Session,
    overdue_hours: int = 24,
):
    cutoff = (
        utc_now()
        - __import__("datetime").timedelta(
            hours=overdue_hours
        )
    )

    return (
        db.query(Transaction)
        .filter(
            Transaction.borrowed_at.isnot(None),
            Transaction.borrowed_at <= cutoff,
            Transaction.returned_at.is_(None),
            Transaction.status.in_(
                ["PENDING", "APPROVED"]
            ),
        )
        .all()
    )


# ============================================================
# OVERVIEW
# ============================================================

def get_overview(
    db: Session,
) -> AnalyticsOverview:

    # --------------------------------------------------------
    # STUDENTS
    # --------------------------------------------------------
    #
    # We intentionally count distinct student IDs from
    # attendance because attendance is the current source
    # of historical student activity available to analytics.
    # --------------------------------------------------------

    total_students = (
        db.query(
            func.count(
                func.distinct(
                    Attendance.student_id
                )
            )
        )
        .scalar()
        or 0
    )

    currently_in_lab = (
        db.query(Attendance)
        .filter(
            Attendance.status == "IN",
            Attendance.exit_time.is_(None),
        )
        .count()
    )

    # --------------------------------------------------------
    # ATTENDANCE
    # --------------------------------------------------------

    total_visits = (
        db.query(Attendance)
        .count()
    )

    # --------------------------------------------------------
    # SESSIONS
    # --------------------------------------------------------

    total_sessions = (
        db.query(LabSession)
        .count()
    )

    active_sessions = (
        db.query(LabSession)
        .filter(
            LabSession.end_time.is_(None)
        )
        .count()
    )

    total_lab_time_seconds = 0

    sessions = (
        db.query(LabSession)
        .all()
    )

    for session in sessions:

        start = make_aware(
            getattr(
                session,
                "start_time",
                None,
            )
        )

        end = make_aware(
            getattr(
                session,
                "end_time",
                None,
            )
        )

        if start is None:
            continue

        if end is None:
            end = utc_now()

        duration = (
            end - start
        ).total_seconds()

        if duration > 0:
            total_lab_time_seconds += int(
                duration
            )

    # --------------------------------------------------------
    # INVENTORY
    # --------------------------------------------------------

    total_inventory_items = (
        db.query(Inventory)
        .count()
    )

    total_inventory_quantity = (
        db.query(
            func.coalesce(
                func.sum(
                    Inventory.quantity
                ),
                0,
            )
        )
        .scalar()
        or 0
    )

    low_stock_items = (
        db.query(Inventory)
        .filter(
            Inventory.quantity
            <= Inventory.minimum_quantity
        )
        .count()
    )

    # --------------------------------------------------------
    # TRANSACTIONS
    # --------------------------------------------------------

    total_transactions = (
        db.query(Transaction)
        .count()
    )

    active_transactions = (
        db.query(Transaction)
        .filter(
            Transaction.status.in_(
                ["PENDING", "APPROVED"]
            )
        )
        .count()
    )

    overdue_transactions = len(
        get_overdue_transactions(db)
    )

    # --------------------------------------------------------
    # ALERTS
    # --------------------------------------------------------

    total_alerts = (
        db.query(Alert)
        .count()
    )

    open_alerts = (
        db.query(Alert)
        .filter(
            Alert.status == "OPEN"
        )
        .count()
    )

    mismatch_alerts = (
        db.query(Alert)
        .filter(
            Alert.alert_type == "COMPONENT_MISMATCH"
        )
        .count()
    )

    unknown_person_alerts = (
        db.query(Alert)
        .filter(
            Alert.alert_type == "UNKNOWN_PERSON"
        )
        .count()
    )

    return AnalyticsOverview(
        total_students=int(
            total_students
        ),

        currently_in_lab=int(
            currently_in_lab
        ),

        total_visits=int(
            total_visits
        ),

        total_sessions=int(
            total_sessions
        ),

        total_lab_time_seconds=int(
            total_lab_time_seconds
        ),

        total_inventory_items=int(
            total_inventory_items
        ),

        total_inventory_quantity=int(
            total_inventory_quantity
        ),

        low_stock_items=int(
            low_stock_items
        ),

        total_transactions=int(
            total_transactions
        ),

        active_transactions=int(
            active_transactions
        ),

        overdue_transactions=int(
            overdue_transactions
        ),

        total_alerts=int(
            total_alerts
        ),

        open_alerts=int(
            open_alerts
        ),

        mismatch_alerts=int(
            mismatch_alerts
        ),

        unknown_person_alerts=int(
            unknown_person_alerts
        ),
    )


# ============================================================
# ATTENDANCE ANALYTICS
# ============================================================

def get_attendance_analytics(
    db: Session,
) -> AttendanceAnalytics:

    today = date.today()

    total_visits = (
        db.query(Attendance)
        .count()
    )

    currently_inside = (
        db.query(Attendance)
        .filter(
            Attendance.status == "IN",
            Attendance.exit_time.is_(None),
        )
        .count()
    )

    today_visits = (
        db.query(Attendance)
        .filter(
            Attendance.attendance_date == today
        )
        .count()
    )

    today_completed_visits = (
        db.query(Attendance)
        .filter(
            Attendance.attendance_date == today,
            Attendance.exit_time.isnot(None),
        )
        .count()
    )

    today_active_visits = (
        db.query(Attendance)
        .filter(
            Attendance.attendance_date == today,
            Attendance.exit_time.is_(None),
        )
        .count()
    )

    first_visit = (
        db.query(
            func.min(
                Attendance.entry_time
            )
        )
        .scalar()
    )

    last_visit = (
        db.query(
            func.max(
                Attendance.entry_time
            )
        )
        .scalar()
    )

    return AttendanceAnalytics(
        total_visits=int(
            total_visits
        ),

        currently_inside=int(
            currently_inside
        ),

        today_visits=int(
            today_visits
        ),

        today_completed_visits=int(
            today_completed_visits
        ),

        today_active_visits=int(
            today_active_visits
        ),

        first_visit=first_visit,

        last_visit=last_visit,
    )


# ============================================================
# SESSION ANALYTICS
# ============================================================

def get_session_analytics(
    db: Session,
) -> SessionAnalytics:

    sessions = (
        db.query(LabSession)
        .all()
    )

    total_sessions = len(
        sessions
    )

    active_sessions = 0

    durations = []

    for session in sessions:

        start = make_aware(
            getattr(
                session,
                "start_time",
                None,
            )
        )

        end = make_aware(
            getattr(
                session,
                "end_time",
                None,
            )
        )

        if start is None:
            continue

        if end is None:

            active_sessions += 1
            end = utc_now()

        duration = int(
            max(
                0,
                (
                    end - start
                ).total_seconds(),
            )
        )

        durations.append(
            duration
        )

    total_lab_time_seconds = sum(
        durations
    )

    if durations:
        average_session_time_seconds = (
            total_lab_time_seconds
            / len(durations)
        )

        longest_session_seconds = max(
            durations
        )

        shortest_session_seconds = min(
            durations
        )

    else:
        average_session_time_seconds = 0.0
        longest_session_seconds = 0
        shortest_session_seconds = 0

    return SessionAnalytics(
        total_sessions=int(
            total_sessions
        ),

        active_sessions=int(
            active_sessions
        ),

        total_lab_time_seconds=int(
            total_lab_time_seconds
        ),

        average_session_time_seconds=float(
            average_session_time_seconds
        ),

        longest_session_seconds=int(
            longest_session_seconds
        ),

        shortest_session_seconds=int(
            shortest_session_seconds
        ),
    )


# ============================================================
# INVENTORY ANALYTICS
# ============================================================

def get_inventory_analytics(
    db: Session,
) -> InventoryAnalytics:

    components = (
        db.query(Inventory)
        .all()
    )

    total_components = len(
        components
    )

    total_quantity = sum(
        int(
            component.quantity
            or 0
        )
        for component in components
    )

    available_components = sum(
        1
        for component in components
        if str(
            component.status
            or ""
        ).upper()
        == "AVAILABLE"
    )

    unavailable_components = (
        total_components
        - available_components
    )

    low_stock_components = sum(
        1
        for component in components
        if int(
            component.quantity
            or 0
        )
        <= int(
            component.minimum_quantity
            or 0
        )
    )

    out_of_stock_components = sum(
        1
        for component in components
        if int(
            component.quantity
            or 0
        )
        <= 0
    )

    categories = {
        str(
            component.category
            or "UNCATEGORIZED"
        )
        for component in components
    }

    return InventoryAnalytics(
        total_components=int(
            total_components
        ),

        total_quantity=int(
            total_quantity
        ),

        available_components=int(
            available_components
        ),

        unavailable_components=int(
            unavailable_components
        ),

        low_stock_components=int(
            low_stock_components
        ),

        out_of_stock_components=int(
            out_of_stock_components
        ),

        total_categories=len(
            categories
        ),
    )


# ============================================================
# TRANSACTION ANALYTICS
# ============================================================

def get_transaction_analytics(
    db: Session,
) -> TransactionAnalytics:

    transactions = (
        db.query(Transaction)
        .all()
    )

    total_transactions = len(
        transactions
    )

    pending_transactions = sum(
        1
        for tx in transactions
        if str(
            tx.status or ""
        ).upper()
        == "PENDING"
    )

    approved_transactions = sum(
        1
        for tx in transactions
        if str(
            tx.status or ""
        ).upper()
        == "APPROVED"
    )

    completed_transactions = sum(
        1
        for tx in transactions
        if str(
            tx.status or ""
        ).upper()
        == "COMPLETED"
    )

    rejected_transactions = sum(
        1
        for tx in transactions
        if str(
            tx.status or ""
        ).upper()
        == "REJECTED"
    )

    cancelled_transactions = sum(
        1
        for tx in transactions
        if str(
            tx.status or ""
        ).upper()
        == "CANCELLED"
    )

    active_transactions = sum(
        1
        for tx in transactions
        if str(
            tx.status or ""
        ).upper()
        in {
            "PENDING",
            "APPROVED",
        }
    )

    overdue_transactions = len(
        get_overdue_transactions(db)
    )

    take_transactions = sum(
        1
        for tx in transactions
        if str(
            tx.action or ""
        ).upper()
        == "TAKE"
    )

    return_transactions = sum(
        1
        for tx in transactions
        if str(
            tx.action or ""
        ).upper()
        == "RETURN"
    )

    matched_transactions = sum(
        1
        for tx in transactions
        if str(
            tx.verification_status
            or ""
        ).upper()
        == "MATCHED"
    )

    mismatched_transactions = sum(
        1
        for tx in transactions
        if str(
            tx.verification_status
            or ""
        ).upper()
        == "MISMATCH"
    )

    return TransactionAnalytics(
        total_transactions=int(
            total_transactions
        ),

        pending_transactions=int(
            pending_transactions
        ),

        approved_transactions=int(
            approved_transactions
        ),

        completed_transactions=int(
            completed_transactions
        ),

        rejected_transactions=int(
            rejected_transactions
        ),

        cancelled_transactions=int(
            cancelled_transactions
        ),

        active_transactions=int(
            active_transactions
        ),

        overdue_transactions=int(
            overdue_transactions
        ),

        take_transactions=int(
            take_transactions
        ),

        return_transactions=int(
            return_transactions
        ),

        matched_transactions=int(
            matched_transactions
        ),

        mismatched_transactions=int(
            mismatched_transactions
        ),
    )


# ============================================================
# ALERT ANALYTICS
# ============================================================

def get_alert_analytics(
    db: Session,
) -> AlertAnalytics:

    alerts = (
        db.query(Alert)
        .all()
    )

    total_alerts = len(
        alerts
    )

    open_alerts = sum(
        1
        for alert in alerts
        if str(
            alert.status or ""
        ).upper()
        == "OPEN"
    )

    acknowledged_alerts = sum(
        1
        for alert in alerts
        if str(
            alert.status or ""
        ).upper()
        == "ACKNOWLEDGED"
    )

    resolved_alerts = sum(
        1
        for alert in alerts
        if str(
            alert.status or ""
        ).upper()
        == "RESOLVED"
    )

    low_stock_alerts = sum(
        1
        for alert in alerts
        if str(
            alert.alert_type or ""
        ).upper()
        == "LOW_STOCK"
    )

    mismatch_alerts = sum(
        1
        for alert in alerts
        if str(
            alert.alert_type or ""
        ).upper()
        == "COMPONENT_MISMATCH"
    )

    unknown_person_alerts = sum(
        1
        for alert in alerts
        if str(
            alert.alert_type or ""
        ).upper()
        == "UNKNOWN_PERSON"
    )

    overdue_alerts = sum(
        1
        for alert in alerts
        if str(
            alert.alert_type or ""
        ).upper()
        == "OVERDUE"
    )

    system_warning_alerts = sum(
        1
        for alert in alerts
        if str(
            alert.alert_type or ""
        ).upper()
        == "SYSTEM_WARNING"
    )

    return AlertAnalytics(
        total_alerts=int(
            total_alerts
        ),

        open_alerts=int(
            open_alerts
        ),

        acknowledged_alerts=int(
            acknowledged_alerts
        ),

        resolved_alerts=int(
            resolved_alerts
        ),

        low_stock_alerts=int(
            low_stock_alerts
        ),

        mismatch_alerts=int(
            mismatch_alerts
        ),

        unknown_person_alerts=int(
            unknown_person_alerts
        ),

        overdue_alerts=int(
            overdue_alerts
        ),

        system_warning_alerts=int(
            system_warning_alerts
        ),
    )


# ============================================================
# COMPLETE DASHBOARD ANALYTICS
# ============================================================

def get_dashboard_analytics(
    db: Session,
) -> AnalyticsDashboardResponse:

    return AnalyticsDashboardResponse(
        overview=get_overview(
            db
        ),

        attendance=get_attendance_analytics(
            db
        ),

        sessions=get_session_analytics(
            db
        ),

        inventory=get_inventory_analytics(
            db
        ),

        transactions=get_transaction_analytics(
            db
        ),

        alerts=get_alert_analytics(
            db
        ),
    )


# ============================================================
# DAILY ATTENDANCE ANALYTICS
# ============================================================

def get_daily_attendance(
    db: Session,
) -> list[DailyVisitAnalytics]:

    rows = (
        db.query(
            Attendance.attendance_date,
            func.count(
                Attendance.attendance_id
            ),
        )
        .group_by(
            Attendance.attendance_date
        )
        .order_by(
            Attendance.attendance_date
        )
        .all()
    )

    result = []

    for attendance_date, visits in rows:

        completed = (
            db.query(Attendance)
            .filter(
                Attendance.attendance_date
                == attendance_date,

                Attendance.exit_time.isnot(
                    None
                ),
            )
            .count()
        )

        active = (
            db.query(Attendance)
            .filter(
                Attendance.attendance_date
                == attendance_date,

                Attendance.exit_time.is_(
                    None
                ),
            )
            .count()
        )

        result.append(
            DailyVisitAnalytics(
                date=str(
                    attendance_date
                ),

                visits=int(
                    visits
                ),

                completed_visits=int(
                    completed
                ),

                active_visits=int(
                    active
                ),
            )
        )

    return result


# ============================================================
# STUDENT ANALYTICS
# ============================================================

def get_student_analytics(
    db: Session,
    student_id: str,
) -> StudentAnalytics:

    # --------------------------------------------------------
    # ATTENDANCE
    # --------------------------------------------------------

    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.student_id
            == student_id
        )
        .order_by(
            Attendance.entry_time
        )
        .all()
    )

    total_visits = len(
        attendance
    )

    currently_in_lab = any(
        record.status == "IN"
        and record.exit_time is None
        for record in attendance
    )

    first_visit = (
        attendance[0].entry_time
        if attendance
        else None
    )

    last_visit = (
        attendance[-1].entry_time
        if attendance
        else None
    )

    # --------------------------------------------------------
    # SESSIONS
    # --------------------------------------------------------

    sessions = (
        db.query(LabSession)
        .filter(
            LabSession.student_id
            == student_id
        )
        .all()
    )

    total_sessions = len(
        sessions
    )

    session_durations = []

    for session in sessions:

        start = make_aware(
            getattr(
                session,
                "start_time",
                None,
            )
        )

        end = make_aware(
            getattr(
                session,
                "end_time",
                None,
            )
        )

        if start is None:
            continue

        if end is None:
            end = utc_now()

        duration = int(
            max(
                0,
                (
                    end - start
                ).total_seconds(),
            )
        )

        session_durations.append(
            duration
        )

    total_lab_time_seconds = sum(
        session_durations
    )

    average_session_time_seconds = (
        total_lab_time_seconds
        / len(session_durations)
        if session_durations
        else 0.0
    )

    # --------------------------------------------------------
    # TRANSACTIONS
    # --------------------------------------------------------

    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.student_id
            == student_id
        )
        .all()
    )

    total_transactions = len(
        transactions
    )

    active_transactions = sum(
        1
        for tx in transactions
        if str(
            tx.status or ""
        ).upper()
        in {
            "PENDING",
            "APPROVED",
        }
    )

    overdue_transactions = sum(
        1
        for tx in transactions
        if (
            tx.borrowed_at is not None
            and tx.returned_at is None
            and make_aware(
                tx.borrowed_at
            )
            <= (
                utc_now()
                - __import__(
                    "datetime"
                ).timedelta(
                    hours=24
                )
            )
            and str(
                tx.status or ""
            ).upper()
            in {
                "PENDING",
                "APPROVED",
            }
        )
    )

    # --------------------------------------------------------
    # ALERTS
    # --------------------------------------------------------

    alerts = (
        db.query(Alert)
        .filter(
            Alert.student_id
            == student_id
        )
        .all()
    )

    total_alerts = len(
        alerts
    )

    mismatch_count = sum(
        1
        for alert in alerts
        if str(
            alert.alert_type or ""
        ).upper()
        == "COMPONENT_MISMATCH"
    )

    unknown_event_count = sum(
        1
        for alert in alerts
        if str(
            alert.alert_type or ""
        ).upper()
        == "UNKNOWN_PERSON"
    )

    return StudentAnalytics(
        student_id=student_id,

        currently_in_lab=bool(
            currently_in_lab
        ),

        total_visits=int(
            total_visits
        ),

        total_sessions=int(
            total_sessions
        ),

        total_lab_time_seconds=int(
            total_lab_time_seconds
        ),

        average_session_time_seconds=float(
            average_session_time_seconds
        ),

        total_transactions=int(
            total_transactions
        ),

        active_transactions=int(
            active_transactions
        ),

        overdue_transactions=int(
            overdue_transactions
        ),

        total_alerts=int(
            total_alerts
        ),

        mismatch_count=int(
            mismatch_count
        ),

        unknown_event_count=int(
            unknown_event_count
        ),

        first_visit=first_visit,

        last_visit=last_visit,
    )