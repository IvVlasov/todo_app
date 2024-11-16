from datetime import datetime, timedelta, timezone

import jwt

from backend.api.v1.auth.models import TokenPayload
from backend.core.models.user import User
from backend.settings import get_settings


def create_access_token(user: User) -> str:
    """Create access token"""
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_LIFETIME_MINUTES
    )
    token_payload = TokenPayload(
        user_id=user.user_id, email=user.email, expire_timestamp=int(expire.timestamp())
    )
    encoded_jwt = jwt.encode(
        token_payload.model_dump(),
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_jwt(token: str) -> TokenPayload:
    """Decode JWT"""
    settings = get_settings()
    decoded_token = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    return TokenPayload(**decoded_token)
