from backend.core.constants import HTTPCodesMessage
from backend.core.utils import generate_example_response


_default_bad_request_example = {
    "summary": "bad request",
    "value": {
        "status": "error",
        "status_code": 400,
        "message": "User already exists",
        "payload": None,
    },
}


_default_ok_example = {
    "summary": "ok",
    "value": {
        "status": "success",
        "status_code": 200,
        "message": "User created",
        "payload": {
            "user_id": 1,
        },
    },
}


default_bad_request_example_response = generate_example_response(
    response_examples=_default_bad_request_example,
    description=HTTPCodesMessage.HTTP_400_BAD_REQUEST,
)

default_ok_example_response = generate_example_response(
    response_examples=_default_ok_example,
    description=HTTPCodesMessage.HTTP_200_OK,
)
