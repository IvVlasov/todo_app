import logging

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.core.models import APIResponse


logger = logging.getLogger(__name__)


class ClassNameAndAllAttrStrMixin:
    """Mixin for correct class __str__ with all attrs"""

    def __str__(self):
        return f"<{self.__class__.__name__}>: {', '.join([f'{k}={v}' for k, v in self.__dict__.items()])}"


async def make_response(
    api_response: BaseModel, status_code: int | None = None
) -> JSONResponse:
    """Prepare API JSONResponse"""
    if isinstance(api_response, APIResponse):
        status_code = api_response.status_code

    if not status_code:
        raise ValueError("status_code not provided")

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(api_response),
    )


def generate_example_response(
    response_examples: list[dict] | dict, description: str = "Success"
) -> dict:
    """Substitution of endpoint response examples in response template description"""
    if isinstance(response_examples, dict):
        response_examples = [response_examples]

    return {
        "description": description,
        "content": {
            "application/json": {
                "examples": {
                    response_example["summary"]: response_example
                    for response_example in response_examples
                },
            },
        },
    }


async def raise_http_exception(status_code: int, message: str, **kwargs):
    """Throws HTTP exception"""
    logger.error(message)

    raise HTTPException(
        status_code=status_code,
        detail=message,
        **kwargs,
    )
