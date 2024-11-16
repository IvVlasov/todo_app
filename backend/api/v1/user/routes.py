import logging

from fastapi import APIRouter, Depends, Request
from fastapi import status as fastapi_status

from backend.api.v1.auth import examples as auth_examples
from backend.api.v1.auth.services.token_validator import AppTokenValidator
from backend.api.v1.user import examples, models
from backend.core.db.repository import UserRepository
from backend.core.models import APIResponse, UserCreate
from backend.core.utils import make_response, raise_http_exception


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post(
    "/create",
    name="user_create",
    responses={
        401: auth_examples.default_unauthorized_example_response,
        403: auth_examples.default_forbidden_example_response,
        400: examples.default_bad_request_example_response,
        500: auth_examples.default_internal_server_error_example_response,
        200: examples.default_ok_example_response,
    },
    dependencies=[
        Depends(AppTokenValidator()),
    ],
)
async def create_user(
    user: UserCreate,
    request: Request,
):
    """Create user"""
    logger.info("Creating user: %s", user)
    user_repository = UserRepository(request.app)
    try:
        user_id = await user_repository.create_user(user)
    except Exception as error:
        logger.error("Error creating user: %s", error)
        return await raise_http_exception(
            status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
        )

    if not user_id:
        return await raise_http_exception(
            status_code=fastapi_status.HTTP_400_BAD_REQUEST,
            message="User already exists",
        )

    return await make_response(
        api_response=APIResponse(
            message="OK",
            payload=models.UserCreateResponse(user_id=user_id),
        ),
    )
