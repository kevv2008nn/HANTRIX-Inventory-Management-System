from datetime import datetime, timezone, timedelta
from typing import Any, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.inventory import Inventory


# ============================================================
# CREATE GENERIC ALERT
# ============================================================

def create_alert(
    db: Session,
    alert_type: str,
    title: str,
    message: str,
    severity: str = "INFO",
    student_id: Optional[str] = None,
    component_id: Optional[str] = None,
    camera_id: Optional[str] = None,
    transaction_id: Optional[UUID] = None,
    metadata: Optional[dict[str, Any]] = None,
):
    alert = Alert(
        alert_type=alert_type,
        title=title,
        message=message,
        severity=severity,
        student_id=student_id,
        component_id=component_id,
        camera_id=camera_id,
        transaction_id=transaction_id,
        status="OPEN",
        event_metadata=metadata,
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


# ============================================================
# GET SINGLE ALERT
# ============================================================

def get_alert(
    db: Session,
    alert_id: UUID,
):
    return (
        db.query(Alert)
        .filter(Alert.alert_id == alert_id)
        .first()
    )


# ============================================================
# GET ALL ALERTS
# ============================================================

def get_all_alerts(
    db: Session,
    status: Optional[str] = None,
    limit: int = 100,
):
    query = db.query(Alert)

    if status:
        query = query.filter(
            Alert.status == status
        )

    return (
        query
        .order_by(Alert.created_at.desc())
        .limit(limit)
        .all()
    )


# ============================================================
# GET OPEN ALERTS
# ============================================================

def get_open_alerts(
    db: Session,
):
    return (
        db.query(Alert)
        .filter(Alert.status == "OPEN")
        .order_by(Alert.created_at.desc())
        .all()
    )


# ============================================================
# ACKNOWLEDGE ALERT
# ============================================================

def acknowledge_alert(
    db: Session,
    alert_id: UUID,
):
    alert = get_alert(
        db=db,
        alert_id=alert_id,
    )

    if not alert:
        return None

    alert.status = "ACKNOWLEDGED"

    db.commit()
    db.refresh(alert)

    return alert


# ============================================================
# RESOLVE ALERT
# ============================================================

def resolve_alert(
    db: Session,
    alert_id: UUID,
):
    alert = get_alert(
        db=db,
        alert_id=alert_id,
    )

    if not alert:
        return None

    alert.status = "RESOLVED"
    alert.resolved_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(alert)

    return alert


# ============================================================
# DELETE ALERT
# ============================================================

def delete_alert(
    db: Session,
    alert_id: UUID,
):
    alert = get_alert(
        db=db,
        alert_id=alert_id,
    )

    if not alert:
        return False

    db.delete(alert)
    db.commit()

    return True


# ============================================================
# LOW STOCK ALERT
# ============================================================

def create_low_stock_alert(
    db: Session,
    component_id: str,
    component_name: str,
    quantity: int,
    minimum_quantity: int,
):
    return create_alert(
        db=db,
        alert_type="LOW_STOCK",
        title="Low Stock Alert",
        message=(
            f"{component_name} stock is low. "
            f"Current quantity: {quantity}, "
            f"minimum required: {minimum_quantity}."
        ),
        severity="HIGH",
        component_id=component_id,
        metadata={
            "quantity": quantity,
            "minimum_quantity": minimum_quantity,
        },
    )


# ============================================================
# CHECK EXISTING LOW STOCK ALERT
# ============================================================

def low_stock_alert_exists(
    db: Session,
    component_id: str,
):
    return (
        db.query(Alert)
        .filter(
            Alert.alert_type == "LOW_STOCK",
            Alert.component_id == component_id,
            Alert.status == "OPEN",
        )
        .first()
    )


# ============================================================
# SCAN LOW STOCK
# ============================================================

def scan_low_stock(
    db: Session,
):
    inventory_items = (
        db.query(Inventory)
        .filter(
            Inventory.quantity
            <= Inventory.minimum_quantity
        )
        .all()
    )

    created_alerts = []

    for item in inventory_items:

        existing_alert = low_stock_alert_exists(
            db=db,
            component_id=item.component_id,
        )

        if existing_alert:
            continue

        alert = create_low_stock_alert(
            db=db,
            component_id=item.component_id,
            component_name=item.component_name,
            quantity=item.quantity,
            minimum_quantity=item.minimum_quantity,
        )

        created_alerts.append(alert)

    return created_alerts


# ============================================================
# COMPONENT MISMATCH ALERT
# ============================================================

def create_mismatch_alert(
    db: Session,
    component_id: str,
    student_id: Optional[str],
    transaction_id: Optional[UUID],
    camera_id: Optional[str],
    expected_component: str,
    detected_component: str,
    confidence: Optional[float] = None,
):
    return create_alert(
        db=db,
        alert_type="MISMATCH",
        title="Component Mismatch Detected",
        message=(
            f"Expected '{expected_component}' "
            f"but detected '{detected_component}'."
        ),
        severity="CRITICAL",
        student_id=student_id,
        component_id=component_id,
        camera_id=camera_id,
        transaction_id=transaction_id,
        metadata={
            "expected_component": expected_component,
            "detected_component": detected_component,
            "confidence": confidence,
        },
    )


# ============================================================
# UNKNOWN PERSON ALERT
# ============================================================

def create_unknown_person_alert(
    db: Session,
    camera_id: str,
    confidence: Optional[float] = None,
):
    return create_alert(
        db=db,
        alert_type="UNKNOWN_PERSON",
        title="Unknown Person Detected",
        message=(
            "An unauthenticated person was "
            "detected in the laboratory."
        ),
        severity="CRITICAL",
        camera_id=camera_id,
        metadata={
            "confidence": confidence,
        },
    )


# ============================================================
# OVERDUE ALERT
# ============================================================

def create_overdue_alert(
    db: Session,
    transaction_id: UUID,
    student_id: str,
    component_id: str,
    borrowed_at,
    overdue_hours: float,
):
    return create_alert(
        db=db,
        alert_type="OVERDUE",
        title="Component Return Overdue",
        message=(
            f"Component '{component_id}' borrowed by "
            f"student '{student_id}' has not been returned "
            f"within the expected time."
        ),
        severity="HIGH",
        student_id=student_id,
        component_id=component_id,
        transaction_id=transaction_id,
        metadata={
            "borrowed_at": (
                borrowed_at.isoformat()
                if borrowed_at
                else None
            ),
            "overdue_hours": round(
                overdue_hours,
                2,
            ),
        },
    )


# ============================================================
# CHECK EXISTING OVERDUE ALERT
# ============================================================

def overdue_alert_exists(
    db: Session,
    transaction_id: UUID,
):
    return (
        db.query(Alert)
        .filter(
            Alert.alert_type == "OVERDUE",
            Alert.transaction_id == transaction_id,
            Alert.status == "OPEN",
        )
        .first()
    )


# ============================================================
# SCAN OVERDUE TRANSACTIONS
# ============================================================

def scan_overdue_transactions(
    db: Session,
    overdue_hours: float = 24.0,
):
    from app.models.transaction import Transaction

    cutoff_time = (
        datetime.now(timezone.utc)
        - timedelta(hours=overdue_hours)
    )

    overdue_transactions = (
        db.query(Transaction)
        .filter(
            Transaction.borrowed_at.isnot(None),
            Transaction.borrowed_at <= cutoff_time,
            Transaction.returned_at.is_(None),
            Transaction.status.in_(
                ["PENDING", "APPROVED"]
            ),
        )
        .all()
    )

    created_alerts = []

    for transaction in overdue_transactions:

        existing_alert = overdue_alert_exists(
            db=db,
            transaction_id=transaction.transaction_id,
        )

        if existing_alert:
            continue

        overdue_duration = (
            datetime.now(timezone.utc)
            - transaction.borrowed_at
        )

        overdue_hours_actual = (
            overdue_duration.total_seconds()
            / 3600
        )

        alert = create_overdue_alert(
            db=db,
            transaction_id=transaction.transaction_id,
            student_id=transaction.student_id,
            component_id=transaction.component_id,
            borrowed_at=transaction.borrowed_at,
            overdue_hours=overdue_hours_actual,
        )

        created_alerts.append(alert)

    return created_alerts