import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.transaction import Transaction
from app.models.transaction_log import TransactionLog
from app.alerts.service import create_mismatch_alert


def utc_now():
    return datetime.now(timezone.utc)


# =========================================================
# GET TRANSACTION
# =========================================================

def get_transaction(
    db: Session,
    transaction_id: uuid.UUID,
):
    return (
        db.query(Transaction)
        .filter(
            Transaction.transaction_id == transaction_id
        )
        .first()
    )


# =========================================================
# GET ACTIVE BORROWED TRANSACTION
#
# Finds the latest APPROVED TAKE for a specific
# student/component that has NOT already been returned.
# =========================================================

def get_active_borrowed_transaction(
    db: Session,
    student_id: str,
    component_id: str,
):
    approved_takes = (
        db.query(Transaction)
        .filter(
            Transaction.student_id == student_id,
            Transaction.component_id == component_id,
            Transaction.action == "TAKE",
            Transaction.status == "APPROVED",
        )
        .order_by(
            Transaction.borrowed_at.desc(),
            Transaction.created_at.desc(),
        )
        .all()
    )

    for take in approved_takes:

        completed_return = (
            db.query(Transaction)
            .filter(
                Transaction.student_id == student_id,
                Transaction.component_id == component_id,
                Transaction.action == "RETURN",
                Transaction.status == "COMPLETED",
                Transaction.returned_at.isnot(None),
                Transaction.returned_at >= take.borrowed_at,
            )
            .order_by(
                Transaction.returned_at.desc()
            )
            .first()
        )

        if not completed_return:
            return take

    return None


# =========================================================
# ACTIVE TRANSACTION FOR STUDENT
#
# Active means:
#
# 1. PENDING transaction
# 2. VERIFYING transaction
# 3. APPROVED TAKE which has NOT been returned
#
# Completed / rejected / cancelled transactions
# are NOT considered active.
# =========================================================

def get_active_transaction_for_student(
    db: Session,
    student_id: str,
):
    # -----------------------------------------------------
    # PENDING / VERIFYING
    # -----------------------------------------------------

    pending = (
        db.query(Transaction)
        .filter(
            Transaction.student_id == student_id,
            Transaction.status.in_(
                ["PENDING", "VERIFYING"]
            ),
        )
        .order_by(
            Transaction.created_at.desc()
        )
        .first()
    )

    if pending:
        return pending

    # -----------------------------------------------------
    # APPROVED TAKE which is still borrowed
    # -----------------------------------------------------

    approved_takes = (
        db.query(Transaction)
        .filter(
            Transaction.student_id == student_id,
            Transaction.action == "TAKE",
            Transaction.status == "APPROVED",
        )
        .order_by(
            Transaction.borrowed_at.desc(),
            Transaction.created_at.desc(),
        )
        .all()
    )

    for take in approved_takes:

        completed_return = (
            db.query(Transaction)
            .filter(
                Transaction.student_id == student_id,
                Transaction.component_id == take.component_id,
                Transaction.action == "RETURN",
                Transaction.status == "COMPLETED",
                Transaction.returned_at.isnot(None),
                Transaction.returned_at >= take.borrowed_at,
            )
            .order_by(
                Transaction.returned_at.desc()
            )
            .first()
        )

        if not completed_return:
            return take

    return None


# =========================================================
# CREATE TRANSACTION LOG
# =========================================================

def create_log(
    db: Session,
    transaction: Transaction,
    event_type: str,
    message: str,
    camera_id: Optional[str] = None,
    confidence: Optional[float] = None,
    metadata: Optional[str] = None,
):
    log = TransactionLog(
        transaction_id=transaction.transaction_id,
        student_id=transaction.student_id,
        component_id=transaction.component_id,
        event_type=event_type,
        message=message,
        camera_id=camera_id,
        confidence=confidence,
        event_metadata=metadata,
    )

    db.add(log)

    return log


# =========================================================
# TAKE
# =========================================================

def create_take_transaction(
    db: Session,
    student_id: str,
    component_id: str,
    quantity: int = 1,
):
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero.",
        )

    # -----------------------------------------------------
    # Student must not have another active transaction
    # -----------------------------------------------------

    active = get_active_transaction_for_student(
        db=db,
        student_id=student_id,
    )

    if active:
        raise HTTPException(
            status_code=409,
            detail="Student already has an active transaction.",
        )

    # -----------------------------------------------------
    # Check inventory
    # -----------------------------------------------------

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.component_id == component_id
        )
        .first()
    )

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Component not found.",
        )

    if inventory.quantity < quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient inventory quantity.",
        )

    # -----------------------------------------------------
    # Create TAKE transaction
    #
    # Inventory is NOT changed here.
    # It changes only after Camera 2 MATCH.
    # -----------------------------------------------------

    transaction = Transaction(
        transaction_id=uuid.uuid4(),
        student_id=student_id,
        component_id=component_id,
        action="TAKE",
        quantity=quantity,
        requested_at=utc_now(),
        status="PENDING",
        verification_status="PENDING",
        expected_rack=inventory.rack,
        expected_shelf=inventory.shelf,
        camera_id=None,
        confidence=None,
        mismatch_reason=None,
    )

    db.add(transaction)

    create_log(
        db=db,
        transaction=transaction,
        event_type="TRANSACTION_CREATED",
        message=(
            f"TAKE transaction created for "
            f"{component_id}. Expected location: "
            f"{inventory.rack}/{inventory.shelf}."
        ),
    )

    db.commit()
    db.refresh(transaction)

    return transaction


# =========================================================
# RETURN
# =========================================================

def create_return_transaction(
    db: Session,
    student_id: str,
    component_id: str,
    quantity: int = 1,
):
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero.",
        )

    # -----------------------------------------------------
    # Find the currently borrowed TAKE
    # -----------------------------------------------------

    active = get_active_borrowed_transaction(
        db=db,
        student_id=student_id,
        component_id=component_id,
    )

    if not active:
        raise HTTPException(
            status_code=404,
            detail=(
                "No active borrowed transaction found "
                "for this component."
            ),
        )

    # -----------------------------------------------------
    # Cannot return more than borrowed
    # -----------------------------------------------------

    if quantity > active.quantity:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Return quantity cannot exceed borrowed "
                f"quantity ({active.quantity})."
            ),
        )

    # -----------------------------------------------------
    # Create RETURN transaction
    #
    # Inventory is NOT changed here.
    # It changes only after Camera 2 MATCH.
    # -----------------------------------------------------

    transaction = Transaction(
        transaction_id=uuid.uuid4(),
        student_id=student_id,
        component_id=component_id,
        action="RETURN",
        quantity=quantity,
        requested_at=utc_now(),
        status="PENDING",
        verification_status="PENDING",
        expected_rack=active.expected_rack,
        expected_shelf=active.expected_shelf,
        camera_id=None,
        confidence=None,
        mismatch_reason=None,
    )

    db.add(transaction)

    create_log(
        db=db,
        transaction=transaction,
        event_type="TRANSACTION_CREATED",
        message=(
            f"RETURN transaction created for "
            f"{component_id}."
        ),
    )

    db.commit()
    db.refresh(transaction)

    return transaction


# =========================================================
# VERIFY TRANSACTION
# =========================================================

def verify_transaction(
    db: Session,
    transaction_id: uuid.UUID,
    detected_component: str,
    camera_id: Optional[str] = None,
    confidence: Optional[float] = None,
):
    transaction = get_transaction(
        db=db,
        transaction_id=transaction_id,
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found.",
        )

    # -----------------------------------------------------
    # Only PENDING / VERIFYING can be verified
    # -----------------------------------------------------

    if transaction.status not in [
        "PENDING",
        "VERIFYING",
    ]:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Transaction cannot be verified "
                f"from status {transaction.status}."
            ),
        )

    # -----------------------------------------------------
    # Store Camera 2 verification information
    # -----------------------------------------------------

    transaction.status = "VERIFYING"
    transaction.verification_status = "VERIFYING"
    transaction.camera_id = camera_id
    transaction.confidence = confidence

    expected_component = transaction.component_id

    # -----------------------------------------------------
    # Get expected inventory item
    # -----------------------------------------------------

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.component_id == expected_component
        )
        .first()
    )

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Expected component no longer exists.",
        )

    # -----------------------------------------------------
    # Determine expected detection label
    # -----------------------------------------------------

    expected_label = (
        inventory.detection_label
        or inventory.component_name
        or expected_component
    )

    detected = detected_component.strip().lower()
    expected = expected_label.strip().lower()

    # =====================================================
    # MATCH
    # =====================================================

    if (
        detected == expected
        or detected == expected_component.lower()
    ):

        transaction.verification_status = "MATCHED"

        # -------------------------------------------------
        # TAKE MATCH
        # -------------------------------------------------

        if transaction.action == "TAKE":

            # Re-check inventory at verification time.
            if inventory.quantity < transaction.quantity:

                transaction.status = "REJECTED"
                transaction.verification_status = "MISMATCH"
                transaction.mismatch_reason = (
                    "Insufficient inventory during verification."
                )

                create_log(
                    db=db,
                    transaction=transaction,
                    event_type="TRANSACTION_REJECTED",
                    message=transaction.mismatch_reason,
                    camera_id=camera_id,
                    confidence=confidence,
                )

                # No inventory modification.

                db.commit()
                db.refresh(transaction)

                return transaction

            # -------------------------------------------------
            # Inventory decreases ONLY after MATCH
            # -------------------------------------------------

            inventory.quantity -= transaction.quantity

            transaction.status = "APPROVED"
            transaction.borrowed_at = utc_now()

            create_log(
                db=db,
                transaction=transaction,
                event_type="TRANSACTION_APPROVED",
                message=(
                    f"TAKE verified successfully. "
                    f"{transaction.quantity} x "
                    f"{transaction.component_id} "
                    f"removed from inventory."
                ),
                camera_id=camera_id,
                confidence=confidence,
            )

        # -------------------------------------------------
        # RETURN MATCH
        # -------------------------------------------------

        elif transaction.action == "RETURN":

            # -------------------------------------------------
            # Inventory increases ONLY after MATCH
            # -------------------------------------------------

            inventory.quantity += transaction.quantity

            transaction.status = "COMPLETED"
            transaction.returned_at = utc_now()

            create_log(
                db=db,
                transaction=transaction,
                event_type="TRANSACTION_COMPLETED",
                message=(
                    f"RETURN verified successfully. "
                    f"{transaction.quantity} x "
                    f"{transaction.component_id} "
                    f"added back to inventory."
                ),
                camera_id=camera_id,
                confidence=confidence,
            )

        db.commit()
        db.refresh(transaction)

        return transaction

    # =====================================================
    # MISMATCH
    # =====================================================

    transaction.status = "REJECTED"
    transaction.verification_status = "MISMATCH"

    transaction.mismatch_reason = (
        f"Expected '{expected_label}', "
        f"but detected '{detected_component}'."
    )

    # -----------------------------------------------------
    # Transaction audit log
    # -----------------------------------------------------

    create_log(
        db=db,
        transaction=transaction,
        event_type="COMPONENT_MISMATCH",
        message=transaction.mismatch_reason,
        camera_id=camera_id,
        confidence=confidence,
    )

    # -----------------------------------------------------
    # 🚨 CREATE MISMATCH ALERT
    #
    # student_id comes from the transaction.
    # For normal student transactions this is STU001,
    # which satisfies the existing FK constraint.
    # -----------------------------------------------------

    create_mismatch_alert(
        db=db,
        component_id=transaction.component_id,
        student_id=transaction.student_id,
        transaction_id=transaction.transaction_id,
        camera_id=camera_id,
        expected_component=expected_label,
        detected_component=detected_component,
        confidence=confidence,
    )

    # -----------------------------------------------------
    # IMPORTANT:
    #
    # Inventory is NOT changed on mismatch.
    # -----------------------------------------------------

    db.commit()
    db.refresh(transaction)

    return transaction


# =========================================================
# CANCEL
# =========================================================

def cancel_transaction(
    db: Session,
    transaction_id: uuid.UUID,
):
    transaction = get_transaction(
        db=db,
        transaction_id=transaction_id,
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found.",
        )

    if transaction.status not in [
        "PENDING",
        "VERIFYING",
    ]:
        raise HTTPException(
            status_code=409,
            detail="Only pending transactions can be cancelled.",
        )

    transaction.status = "CANCELLED"
    transaction.verification_status = "CANCELLED"

    create_log(
        db=db,
        transaction=transaction,
        event_type="TRANSACTION_CANCELLED",
        message="Transaction cancelled.",
    )

    db.commit()
    db.refresh(transaction)

    return transaction