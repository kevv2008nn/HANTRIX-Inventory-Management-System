from uuid import UUID
from pydantic import BaseModel


class BorrowItem(BaseModel):

    student_id: UUID
    component_id: UUID
    quantity: int


class ReturnItem(BaseModel):

    transaction_id: UUID