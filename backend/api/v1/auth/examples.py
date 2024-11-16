from backend.core.constants import HTTPCodesMessage
from backend.core.utils import generate_example_response


_default_forbidden_example = {
    "summary": "forbidden",
    "value": {
        "status": "error",
        "status_code": 403,
        "message": "Provided credentials are not valid",
        "payload": None,
    },
}

_default_unauthorized_example = {
    "summary": "unauthorized",
    "value": {
        "status": "error",
        "status_code": 401,
        "message": "Credentials are not provided",
        "payload": None,
    },
}

_default_internal_server_error_example = {
    "summary": "internal server error",
    "value": {
        "status": "error",
        "status_code": 500,
        "message": "Internal server error",
        "payload": None,
    },
}

_default_ok_example = {
    "summary": "ok",
    "value": {"token": "token"},
}

default_forbidden_example_response = generate_example_response(
    response_examples=_default_forbidden_example,
    description=HTTPCodesMessage.HTTP_403_FORBIDDEN,
)

default_unauthorized_example_response = generate_example_response(
    response_examples=_default_unauthorized_example,
    description=HTTPCodesMessage.HTTP_401_UNAUTHORIZED,
)

default_ok_example_response = generate_example_response(
    response_examples=_default_ok_example,
    description=HTTPCodesMessage.HTTP_200_OK,
)

default_internal_server_error_example_response = generate_example_response(
    response_examples=_default_internal_server_error_example,
    description=HTTPCodesMessage.HTTP_500_INTERNAL_SERVER_ERROR,
)
