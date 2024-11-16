from typing import Annotated

from fastapi import Depends, Request, Security
from fastapi.security import HTTPAuthorizationCredentials

from backend.api.v1.auth.security import jwt_scheme
from backend.api.v1.auth.services.jwt_token import decode_jwt
from backend.core.db.repository.user import UserRepository
from backend.core.models.user import User


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(jwt_scheme)],
    request: Request,
):
    user_repository = UserRepository(request.app)
    token_data = decode_jwt(token.credentials)
    user = await user_repository.get_user_by_token_payload(token_data)
    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user)],
):
    return current_user
