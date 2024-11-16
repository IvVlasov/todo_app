from pydantic import BaseModel


class UserCreateResponse(BaseModel):
    """User create response model"""

    user_id: int
