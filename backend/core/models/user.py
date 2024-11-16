import hashlib

from pydantic import BaseModel, field_validator


class User(BaseModel):
    """User model"""

    user_id: int
    email: str
    password: str


class UserResponse(BaseModel):
    """User response model"""

    user_id: int
    email: str


class UserCreate(BaseModel):
    """User create response model"""

    email: str
    password: str

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
