from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.borrow_return.models import BorrowTransaction
from app.models.inventory import Inventory
from app.student_profile.models import StudentProfile
from app.notifications.models import Notification


def borrow_component(data, db: Session):

    # Find component
    component = (
        db.query(Inventory)
        .filter(
            Inventory.component_id == data.component_id
        )
        .first()
    )

    if component is None:
        raise HTTPException(
            status_code=404,
            detail="Component Not Found"
        )

    # Check quantity
    if data.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    if component.quantity < data.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient Stock"
        )

    # Reduce stock
    component.quantity -= data.quantity

    # Update status
    if component.quantity == 0:
        component.status = "Out of Stock"

    elif component.quantity <= component.minimum_quantity:
        component.status = "Low Stock"

    else:
        component.status = "Available"

    # Create borrow transaction
    transaction = BorrowTransaction(
        student_id=data.student_id,
        component_id=data.component_id,
        quantity=data.quantity,
        borrow_time=datetime.now(),
        status="BORROWED"
    )

    db.add(transaction)

    # Update student statistics
    profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.student_id == data.student_id
        )
        .first()
    )

    if profile:
        profile.total_components_borrowed += data.quantity

    # Notification
    notification = Notification(
        title="Component Borrowed",
        message=(
            f"Student {data.student_id} "
            f"borrowed {data.quantity} "
            f"unit(s) of {component.component_name}."
        ),
        receiver="FACULTY",
        type="BORROW"
    )

    db.add(notification)

    db.commit()
    db.refresh(transaction)

    return {
        "success": True,
        "message": "Component borrowed successfully",
        "transaction_id": str(transaction.transaction_id),
        "component_id": str(component.component_id),
        "component_name": component.component_name,
        "quantity": data.quantity,
        "remaining_stock": component.quantity,
        "status": transaction.status
    }


def return_component(data, db: Session):

    # Find transaction
    transaction = (
        db.query(BorrowTransaction)
        .filter(
            BorrowTransaction.transaction_id
            == data.transaction_id
        )
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction Not Found"
        )

    # Prevent returning twice
    if transaction.status == "RETURNED":
        raise HTTPException(
            status_code=400,
            detail="Component already returned"
        )

    # Find component
    component = (
        db.query(Inventory)
        .filter(
            Inventory.component_id
            == transaction.component_id
        )
        .first()
    )

    if component is None:
        raise HTTPException(
            status_code=404,
            detail="Component Not Found"
        )

    # Restore stock
    component.quantity += transaction.quantity

    # Update component status
    if component.quantity <= component.minimum_quantity:
        component.status = "Low Stock"
    else:
        component.status = "Available"

    # Close transaction
    transaction.return_time = datetime.now()
    transaction.status = "RETURNED"

    # Notification
    notification = Notification(
        title="Component Returned",
        message=(
            f"Student {transaction.student_id} "
            f"returned {transaction.quantity} "
            f"unit(s) of {component.component_name}."
        ),
        receiver="FACULTY",
        type="RETURN"
    )

    db.add(notification)

    db.commit()
    db.refresh(transaction)

    return {
        "success": True,
        "message": "Component returned successfully",
        "transaction_id": str(transaction.transaction_id),
        "component_id": str(component.component_id),
        "component_name": component.component_name,
        "quantity": transaction.quantity,
        "current_stock": component.quantity,
        "status": transaction.status
    }


def student_borrowed_components(
    student_id,
    db: Session
):

    transactions = (
        db.query(BorrowTransaction)
        .filter(
            BorrowTransaction.student_id == student_id,
            BorrowTransaction.status == "BORROWED"
        )
        .all()
    )

    result = []

    for transaction in transactions:

        component = (
            db.query(Inventory)
            .filter(
                Inventory.component_id
                == transaction.component_id
            )
            .first()
        )

        if component is None:
            continue

        result.append({
            "transaction_id": str(
                transaction.transaction_id
            ),
            "component_id": str(
                component.component_id
            ),
            "component_name": component.component_name,
            "quantity": transaction.quantity,
            "borrow_time": transaction.borrow_time,
            "status": transaction.status
        })

    return result