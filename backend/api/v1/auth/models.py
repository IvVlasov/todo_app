from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Get token API response"""

    token: str


class TokenPayload(BaseModel):
    """Decoded token"""

    user_id: int
    email: str
    expire_timestamp: int
