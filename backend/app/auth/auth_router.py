from fastapi import APIRouter, HTTPException

from app.auth.auth_schema import LoginRequest
from app.auth.security import (
    verify_password,
    create_access_token,
    hash_password
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Store the plain password separately
ADMIN_EMAIL = "admin@smartlab.com"
ADMIN_PASSWORD = "admin123"

# Hash it once when the application starts
HASHED_PASSWORD = hash_password(ADMIN_PASSWORD)


@router.post("/login")
def login(data: LoginRequest):

    if data.email != ADMIN_EMAIL:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not verify_password(
        data.password,
        HASHED_PASSWORD
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    token = create_access_token({
        "email": ADMIN_EMAIL,
        "role": "ADMIN"
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }