import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi import status as fastapi_status

from backend.api.v1.auth import examples as auth_examples
from backend.api.v1.auth.services.jwt_token_validator import JWTTokenValidator
from backend.api.v1.tasks import examples, models
from backend.api.v1.user.services.user_service import get_current_active_user
from backend.core.constants import TaskStatus
from backend.core.db.repository import TaskRepository
from backend.core.models import Task, TaskCreate, TaskUpdate, User
from backend.core.models.api_response import APIResponse
from backend.core.utils import make_response, raise_http_exception


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/task",
    tags=["task"],
)


@router.post(
    "/create",
    name="task_create",
    responses={
        401: auth_examples.default_unauthorized_example_response,
        403: auth_examples.default_forbidden_example_response,
        500: auth_examples.default_internal_server_error_example_response,
        200: examples.default_ok_example_response,
    },
    dependencies=[
        Depends(JWTTokenValidator()),
    ],
)
async def create_task(
    task_create: TaskCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    """Create task"""
    logger.info("User: %s, Creating task: %s", current_user.user_id, task_create)
    task_repository = TaskRepository(request.app)
    try:
        task = Task(**task_create.model_dump(), user_id=current_user.user_id)
    except Exception as error:
        logger.error("Error creating task: %s", error)
        return await raise_http_exception(
            status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
        )
    await task_repository.create_task(task)
    return await make_response(
        api_response=APIResponse(
            message="OK",
        ),
    )


@router.get(
    "/get_user_tasks",
    name="get_user_tasks",
    dependencies=[
        Depends(JWTTokenValidator()),
    ],
    responses={
        401: auth_examples.default_unauthorized_example_response,
        403: auth_examples.default_forbidden_example_response,
        500: auth_examples.default_internal_server_error_example_response,
        200: examples.default_ok_example_response,
    },
)
async def get_user_tasks(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    """Get user tasks"""
    logger.info("User: %s, Getting user tasks", current_user.user_id)
    task_repository = TaskRepository(request.app)
    tasks = await task_repository.get_tasks_by_user_id(current_user.user_id)
    return await make_response(
        api_response=APIResponse(
            message="OK",
            payload=models.UserTasksResponse(tasks=tasks),
        ),
    )


@router.patch(
    "/update/{task_id}",
    name="task_update",
    responses={
        400: examples.default_bad_request_example_response,
        401: auth_examples.default_unauthorized_example_response,
        403: auth_examples.default_forbidden_example_response,
        500: auth_examples.default_internal_server_error_example_response,
        200: examples.default_ok_example_response,
    },
    dependencies=[
        Depends(JWTTokenValidator()),
    ],
)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Update task"""
    logger.info("User: %s, Updating task: %s", current_user.user_id, task_update)
    task_repository = TaskRepository(request.app)
    if task_update.status and not TaskStatus.has_member_key(task_update.status):
        return await raise_http_exception(
            status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Invalid status value",
        )
    try:
        await task_repository.update_task(task_id, task_update)
    except Exception as error:
        logger.error("Error updating task: %s", error)
        return await raise_http_exception(
            status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
        )
    return await make_response(
        api_response=APIResponse(
            message="OK",
        ),
    )


@router.delete(
    "/delete/{task_id}",
    name="task_delete",
    responses={
        401: auth_examples.default_unauthorized_example_response,
        403: auth_examples.default_forbidden_example_response,
        500: auth_examples.default_internal_server_error_example_response,
        200: examples.default_ok_example_response,
    },
    dependencies=[
        Depends(JWTTokenValidator()),
    ],
)
async def delete_task(
    task_id: int,
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Delete task"""
    logger.info("User: %s, Deleting task: %s", current_user.user_id, task_id)
    task_repository = TaskRepository(request.app)
    try:
        await task_repository.delete_task(task_id)
    except Exception as error:
        logger.error("Error deleting task: %s", error)
        await raise_http_exception(
            status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
        )
    return await make_response(
        api_response=APIResponse(
            message="OK",
        ),
    )
