from typing import Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.alert import (
    AlertCreate,
    AlertResponse,
)

from app.alerts.service import (
    acknowledge_alert,
    create_alert,
    create_mismatch_alert,
    create_unknown_person_alert,
    get_alert,
    get_all_alerts,
    get_open_alerts,
    resolve_alert,
    scan_low_stock,
    scan_overdue_transactions,
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


# ============================================================
# CREATE ALERT
# ============================================================

@router.post(
    "/",
    response_model=AlertResponse,
)
def create_alert_endpoint(
    data: AlertCreate,
    db: Session = Depends(get_db),
):
    return create_alert(
        db=db,
        alert_type=data.alert_type,
        title=data.title,
        message=data.message,
        severity=data.severity,
        student_id=data.student_id,
        component_id=data.component_id,
        camera_id=data.camera_id,
        transaction_id=data.transaction_id,
        metadata=data.metadata,
    )


# ============================================================
# GET ALL ALERTS
# ============================================================

@router.get(
    "/",
    response_model=list[AlertResponse],
)
def list_alerts(
    status: Optional[str] = Query(
        default=None
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    db: Session = Depends(get_db),
):
    return get_all_alerts(
        db=db,
        status=status,
        limit=limit,
    )


# ============================================================
# GET OPEN ALERTS
# ============================================================

@router.get(
    "/open",
    response_model=list[AlertResponse],
)
def list_open_alerts(
    db: Session = Depends(get_db),
):
    return get_open_alerts(db)


# ============================================================
# SCAN LOW STOCK
# ============================================================

@router.post(
    "/scan/low-stock",
    response_model=list[AlertResponse],
)
def scan_low_stock_endpoint(
    db: Session = Depends(get_db),
):
    return scan_low_stock(db)


# ============================================================
# SCAN OVERDUE TRANSACTIONS
# ============================================================

@router.post(
    "/scan/overdue",
    response_model=list[AlertResponse],
)
def scan_overdue_endpoint(
    overdue_hours: float = Query(
        default=24.0,
        gt=0,
    ),
    db: Session = Depends(get_db),
):
    return scan_overdue_transactions(
        db=db,
        overdue_hours=overdue_hours,
    )


# ============================================================
# GET SINGLE ALERT
# ============================================================

@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
)
def get_alert_endpoint(
    alert_id: UUID,
    db: Session = Depends(get_db),
):
    alert = get_alert(
        db=db,
        alert_id=alert_id,
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return alert


# ============================================================
# ACKNOWLEDGE ALERT
# ============================================================

@router.patch(
    "/{alert_id}/acknowledge",
    response_model=AlertResponse,
)
def acknowledge_alert_endpoint(
    alert_id: UUID,
    db: Session = Depends(get_db),
):
    alert = acknowledge_alert(
        db=db,
        alert_id=alert_id,
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return alert


# ============================================================
# RESOLVE ALERT
# ============================================================

@router.patch(
    "/{alert_id}/resolve",
    response_model=AlertResponse,
)
def resolve_alert_endpoint(
    alert_id: UUID,
    db: Session = Depends(get_db),
):
    alert = resolve_alert(
        db=db,
        alert_id=alert_id,
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return alert


# ============================================================
# TEST MISMATCH ALERT
# ============================================================

@router.post(
    "/test/mismatch",
    response_model=AlertResponse,
)
def test_mismatch_alert(
    db: Session = Depends(get_db),
):
    return create_mismatch_alert(
        db=db,
        component_id="ESP32-001",
        student_id="TEST-STUDENT",
        transaction_id=None,
        camera_id="camera_2",
        expected_component="ESP32",
        detected_component="Arduino UNO",
        confidence=0.94,
    )


# ============================================================
# TEST UNKNOWN PERSON ALERT
# ============================================================

@router.post(
    "/test/unknown",
    response_model=AlertResponse,
)
def test_unknown_person_alert(
    db: Session = Depends(get_db),
):
    return create_unknown_person_alert(
        db=db,
        camera_id="camera_1",
        confidence=0.87,
    )