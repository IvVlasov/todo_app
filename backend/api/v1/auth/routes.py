import logging

from fastapi import APIRouter, Depends, Request
from fastapi import status as fastapi_status

from backend.api.v1.auth import examples
from backend.api.v1.auth.models import TokenResponse
from backend.api.v1.auth.services.jwt_token import create_access_token
from backend.api.v1.auth.services.token_validator import AppTokenValidator
from backend.core.db.repository import UserRepository
from backend.core.models import UserCreate
from backend.core.utils import make_response, raise_http_exception


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/token",
    name="auth_get_token",
    responses={
        401: examples.default_unauthorized_example_response,
        403: examples.default_forbidden_example_response,
        200: examples.default_ok_example_response,
    },
    dependencies=[
        Depends(AppTokenValidator()),
    ],
)
async def get_token(
    user: UserCreate,
    request: Request,
):
    """Get token"""
    user_repository = UserRepository(request.app)
    user_data = await user_repository.get_user_by_credentials(user.email, user.password)
    if not user_data:
        return await raise_http_exception(
            status_code=fastapi_status.HTTP_401_UNAUTHORIZED,
            message="Invalid user credentials",
        )
    token = create_access_token(user_data)
    return await make_response(
        api_response=TokenResponse(token=token),
        status_code=fastapi_status.HTTP_200_OK,
    )
