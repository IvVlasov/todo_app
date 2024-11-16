from typing import Any

from fastapi import status as fastapi_status
from pydantic import BaseModel

from backend.core.constants import APIResponseStatus


class APIResponse(BaseModel):
    """Base API response"""

    status: str = APIResponseStatus.SUCCESS
    status_code: int = fastapi_status.HTTP_200_OK
    message: str | None = None
    payload: Any | None = None


class ErrorAPIResponse(APIResponse):
    """Error API response"""

    status: str = APIResponseStatus.ERROR
