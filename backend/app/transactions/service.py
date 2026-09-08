from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.transaction import Transaction
from app.models.transaction_log import TransactionLog


# ============================================================
# HELPERS
# ============================================================

def get_transaction(
    db: Session,
    transaction_id,
):
    return (
        db.query(Transaction)
        .filter(
            Transaction.transaction_id
            == transaction_id
        )
        .first()
    )


def get_active_transaction_for_student(
    db: Session,
    student_id: str,
):

    return (
        db.query(Transaction)
        .filter(
            Transaction.student_id == student_id,
            Transaction.status.in_(
                [
                    "PENDING",
                    "VERIFYING",
                ]
            ),
        )
        .order_by(
            Transaction.created_at.desc()
        )
        .first()
    )


def create_log(
    db: Session,
    transaction,
    event_type: str,
    message: str,
    confidence=None,
    camera_id=None,
    metadata=None,
):

    log = TransactionLog(
        transaction_id=transaction.transaction_id,
        student_id=transaction.student_id,
        component_id=transaction.component_id,
        event_type=event_type,
        message=message,
        confidence=confidence,
        camera_id=camera_id,
        metadata=metadata,
    )

    db.add(log)


# ============================================================
# TAKE
# ============================================================

def create_take_transaction(
    db: Session,
    student_id: str,
    component_id: str,
    quantity: int,
):

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.component_id
            == component_id
        )
        .first()
    )

    if not inventory:
        raise ValueError(
            "Component not found"
        )

    if inventory.quantity < quantity:

        raise ValueError(
            f"Insufficient stock. "
            f"Available: {inventory.quantity}"
        )

    active = get_active_transaction_for_student(
        db,
        student_id,
    )

    if active:

        raise ValueError(
            "Student already has an active transaction"
        )

    transaction = Transaction(
        student_id=student_id,
        component_id=component_id,
        action="TAKE",
        quantity=quantity,
        status="PENDING",
        verification_status="PENDING",
        expected_rack=inventory.rack,
        expected_shelf=inventory.shelf,
        camera_id="camera_2",
    )

    db.add(transaction)

    db.flush()

    create_log(
        db,
        transaction,
        "TAKE_REQUESTED",
        f"TAKE requested for {inventory.component_name}",
    )

    db.commit()

    db.refresh(transaction)

    return transaction


# ============================================================
# RETURN
# ============================================================

def create_return_transaction(
    db: Session,
    student_id: str,
    component_id: str,
    quantity: int,
):

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.component_id
            == component_id
        )
        .first()
    )

    if not inventory:

        raise ValueError(
            "Component not found"
        )

    active = get_active_transaction_for_student(
        db,
        student_id,
    )

    if active:

        raise ValueError(
            "Student already has an active transaction"
        )

    transaction = Transaction(
        student_id=student_id,
        component_id=component_id,
        action="RETURN",
        quantity=quantity,
        status="PENDING",
        verification_status="PENDING",
        expected_rack=inventory.rack,
        expected_shelf=inventory.shelf,
        camera_id="camera_2",
    )

    db.add(transaction)

    db.flush()

    create_log(
        db,
        transaction,
        "RETURN_REQUESTED",
        f"RETURN requested for {inventory.component_name}",
    )

    db.commit()

    db.refresh(transaction)

    return transaction


# ============================================================
# VERIFICATION
# ============================================================

def verify_transaction(
    db: Session,
    transaction_id,
    detected_label: str,
    confidence: float,
    camera_id: str | None = None,
):

    transaction = get_transaction(
        db,
        transaction_id,
    )

    if not transaction:

        raise ValueError(
            "Transaction not found"
        )

    if transaction.status not in [
        "PENDING",
        "VERIFYING",
    ]:

        raise ValueError(
            "Transaction is no longer active"
        )

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.component_id
            == transaction.component_id
        )
        .first()
    )

    if not inventory:

        raise ValueError(
            "Expected component no longer exists"
        )

    transaction.status = "VERIFYING"

    transaction.camera_id = (
        camera_id or transaction.camera_id
    )

    transaction.confidence = confidence

    expected_label = (
        inventory.detection_label
        or inventory.component_name
    )

    # --------------------------------------------------------
    # MATCH
    # --------------------------------------------------------

    if (
        detected_label.strip().lower()
        == expected_label.strip().lower()
    ):

        transaction.verification_status = "MATCHED"

        transaction.status = "APPROVED"

        if transaction.action == "TAKE":

            if (
                inventory.quantity
                < transaction.quantity
            ):

                transaction.status = "REJECTED"
                transaction.verification_status = "FAILED"

                transaction.mismatch_reason = (
                    "Insufficient stock during verification"
                )

                create_log(
                    db,
                    transaction,
                    "VERIFICATION_FAILED",
                    transaction.mismatch_reason,
                    confidence,
                    camera_id,
                )

                db.commit()

                return transaction

            inventory.quantity -= (
                transaction.quantity
            )

            transaction.borrowed_at = (
                datetime.now(timezone.utc)
            )

            create_log(
                db,
                transaction,
                "INVENTORY_DECREMENTED",
                "Inventory decreased after successful TAKE verification",
                confidence,
                camera_id,
            )

        else:

            inventory.quantity += (
                transaction.quantity
            )

            transaction.returned_at = (
                datetime.now(timezone.utc)
            )

            transaction.status = "COMPLETED"

            create_log(
                db,
                transaction,
                "INVENTORY_INCREMENTED",
                "Inventory increased after successful RETURN verification",
                confidence,
                camera_id,
            )

        create_log(
            db,
            transaction,
            "VERIFICATION_MATCHED",
            f"Detected {detected_label}; expected {expected_label}",
            confidence,
            camera_id,
        )

    # --------------------------------------------------------
    # MISMATCH
    # --------------------------------------------------------

    else:

        transaction.verification_status = "MISMATCH"

        transaction.status = "REJECTED"

        transaction.mismatch_reason = (
            f"Expected '{expected_label}' "
            f"but detected '{detected_label}'"
        )

        create_log(
            db,
            transaction,
            "MISMATCH",
            transaction.mismatch_reason,
            confidence,
            camera_id,
        )

    db.commit()

    db.refresh(transaction)

    return transaction


# ============================================================
# CANCEL
# ============================================================

def cancel_transaction(
    db: Session,
    transaction_id,
):

    transaction = get_transaction(
        db,
        transaction_id,
    )

    if not transaction:

        return None

    if transaction.status not in [
        "PENDING",
        "VERIFYING",
    ]:

        raise ValueError(
            "Transaction cannot be cancelled"
        )

    transaction.status = "CANCELLED"

    create_log(
        db,
        transaction,
        "TRANSACTION_CANCELLED",
        "Transaction cancelled",
    )

    db.commit()

    db.refresh(transaction)

    return transaction