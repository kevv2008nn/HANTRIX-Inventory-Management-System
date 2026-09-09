from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# OVERVIEW
# ============================================================

class AnalyticsOverview(BaseModel):
    total_students: int
    currently_in_lab: int

    total_visits: int
    total_sessions: int
    total_lab_time_seconds: int

    total_inventory_items: int
    total_inventory_quantity: int
    low_stock_items: int

    total_transactions: int
    active_transactions: int
    overdue_transactions: int

    total_alerts: int
    open_alerts: int
    mismatch_alerts: int
    unknown_person_alerts: int


# ============================================================
# ATTENDANCE ANALYTICS
# ============================================================

class AttendanceAnalytics(BaseModel):
    total_visits: int
    currently_inside: int

    today_visits: int
    today_completed_visits: int
    today_active_visits: int

    first_visit: Optional[datetime] = None
    last_visit: Optional[datetime] = None


# ============================================================
# SESSION ANALYTICS
# ============================================================

class SessionAnalytics(BaseModel):
    total_sessions: int
    active_sessions: int

    total_lab_time_seconds: int
    average_session_time_seconds: float

    longest_session_seconds: int
    shortest_session_seconds: int


# ============================================================
# INVENTORY ANALYTICS
# ============================================================

class InventoryAnalytics(BaseModel):
    total_components: int
    total_quantity: int

    available_components: int
    unavailable_components: int

    low_stock_components: int
    out_of_stock_components: int

    total_categories: int


# ============================================================
# TRANSACTION ANALYTICS
# ============================================================

class TransactionAnalytics(BaseModel):
    total_transactions: int

    pending_transactions: int
    approved_transactions: int
    completed_transactions: int
    rejected_transactions: int
    cancelled_transactions: int

    active_transactions: int
    overdue_transactions: int

    take_transactions: int
    return_transactions: int

    matched_transactions: int
    mismatched_transactions: int


# ============================================================
# ALERT ANALYTICS
# ============================================================

class AlertAnalytics(BaseModel):
    total_alerts: int
    open_alerts: int
    acknowledged_alerts: int
    resolved_alerts: int

    low_stock_alerts: int
    mismatch_alerts: int
    unknown_person_alerts: int
    overdue_alerts: int
    system_warning_alerts: int


# ============================================================
# STUDENT ANALYTICS
# ============================================================

class StudentAnalytics(BaseModel):
    student_id: str

    currently_in_lab: bool

    total_visits: int
    total_sessions: int

    total_lab_time_seconds: int
    average_session_time_seconds: float

    total_transactions: int
    active_transactions: int
    overdue_transactions: int

    total_alerts: int
    mismatch_count: int
    unknown_event_count: int

    first_visit: Optional[datetime] = None
    last_visit: Optional[datetime] = None


# ============================================================
# DAILY VISIT ANALYTICS
# ============================================================

class DailyVisitAnalytics(BaseModel):
    date: str
    visits: int
    completed_visits: int
    active_visits: int


# ============================================================
# ANALYTICS RESPONSE
# ============================================================

class AnalyticsDashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    overview: AnalyticsOverview
    attendance: AttendanceAnalytics
    sessions: SessionAnalytics
    inventory: InventoryAnalytics
    transactions: TransactionAnalytics
    alerts: AlertAnalytics