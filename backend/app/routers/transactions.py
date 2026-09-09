from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.transaction import (
    TakeRequest,
    ReturnRequest,
    VerificationRequest,
    TransactionResponse,
)

from app.transactions.service import (
    create_take_transaction,
    create_return_transaction,
    get_transaction,
    verify_transaction,
    cancel_transaction,
)


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


# =========================================================
# TAKE
# =========================================================

@router.post(
    "/take",
    response_model=TransactionResponse,
)
def take_component(
    data: TakeRequest,
    db: Session = Depends(get_db),
):

    return create_take_transaction(
        db=db,
        student_id=data.student_id,
        component_id=data.component_id,
        quantity=data.quantity,
    )


# =========================================================
# RETURN
# =========================================================

@router.post(
    "/return",
    response_model=TransactionResponse,
)
def return_component(
    data: ReturnRequest,
    db: Session = Depends(get_db),
):

    return create_return_transaction(
        db=db,
        student_id=data.student_id,
        component_id=data.component_id,
        quantity=data.quantity,
    )


# =========================================================
# GET TRANSACTION
# =========================================================

@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction_endpoint(
    transaction_id: UUID,
    db: Session = Depends(get_db),
):

    return get_transaction(
        db=db,
        transaction_id=transaction_id,
    )


# =========================================================
# CAMERA-2 VERIFY
# =========================================================

@router.post(
    "/{transaction_id}/verify",
    response_model=TransactionResponse,
)
def verify_transaction_endpoint(
    transaction_id: UUID,
    data: VerificationRequest,
    db: Session = Depends(get_db),
):

    # -----------------------------------------------------
    # CAMERA-2 ONLY
    # -----------------------------------------------------

    camera_id = (
        data.camera_id
        or "camera_2"
    )

    if camera_id.lower() != "camera_2":

        raise HTTPException(
            status_code=400,
            detail=(
                "Transaction verification "
                "must be performed by camera_2."
            ),
        )

    # -----------------------------------------------------
    # VERIFY TRANSACTION
    # -----------------------------------------------------

    return verify_transaction(
        db=db,
        transaction_id=transaction_id,
        detected_component=data.detected_component,
        camera_id=camera_id,
        confidence=data.confidence,
    )


# =========================================================
# CANCEL
# =========================================================

@router.post(
    "/{transaction_id}/cancel",
    response_model=TransactionResponse,
)
def cancel_transaction_endpoint(
    transaction_id: UUID,
    db: Session = Depends(get_db),
):

    return cancel_transaction(
        db=db,
        transaction_id=transaction_id,
    )