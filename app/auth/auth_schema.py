from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class RegisterAdmin(BaseModel):
    name: str
    email: EmailStr
    password: str


class RegisterFaculty(BaseModel):
    name: str
    email: EmailStr
    department: str
    password: str