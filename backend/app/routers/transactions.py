from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

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


# ============================================================
# TAKE
# ============================================================

@router.post(
    "/take",
    response_model=TransactionResponse,
)
def take_component(
    data: TakeRequest,
    db: Session = Depends(get_db),
):

    try:

        return create_take_transaction(
            db=db,
            student_id=data.student_id,
            component_id=data.component_id,
            quantity=data.quantity,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ============================================================
# RETURN
# ============================================================

@router.post(
    "/return",
    response_model=TransactionResponse,
)
def return_component(
    data: ReturnRequest,
    db: Session = Depends(get_db),
):

    try:

        return create_return_transaction(
            db=db,
            student_id=data.student_id,
            component_id=data.component_id,
            quantity=data.quantity,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ============================================================
# GET
# ============================================================

@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction_by_id(
    transaction_id: UUID,
    db: Session = Depends(get_db),
):

    transaction = get_transaction(
        db,
        transaction_id,
    )

    if not transaction:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    return transaction


# ============================================================
# VERIFY
# ============================================================

@router.post(
    "/{transaction_id}/verify",
    response_model=TransactionResponse,
)
def verify(
    transaction_id: UUID,
    data: VerificationRequest,
    db: Session = Depends(get_db),
):

    try:

        return verify_transaction(
            db=db,
            transaction_id=transaction_id,
            detected_label=data.detected_label,
            confidence=data.confidence,
            camera_id=data.camera_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ============================================================
# CANCEL
# ============================================================

@router.post(
    "/{transaction_id}/cancel",
    response_model=TransactionResponse,
)
def cancel(
    transaction_id: UUID,
    db: Session = Depends(get_db),
):

    try:

        transaction = cancel_transaction(
            db,
            transaction_id,
        )

        if not transaction:

            raise HTTPException(
                status_code=404,
                detail="Transaction not found",
            )

        return transaction

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )