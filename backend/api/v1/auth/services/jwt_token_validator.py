import logging

from fastapi import Depends, Request, status
from fastapi.security import HTTPAuthorizationCredentials

from backend.api.v1.auth import constants
from backend.api.v1.auth.security import jwt_scheme
from backend.api.v1.user.services.user_service import get_current_user
from backend.core.utils import raise_http_exception
from backend.settings import get_settings


logger = logging.getLogger(__name__)


class JWTTokenValidatorService:
    """Token validator Service"""

    def __init__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(jwt_scheme),
    ) -> None:
        self._settings = get_settings()
        self.request = request
        self._credentials = credentials

    async def validate(self) -> None:
        """Process of token validation"""
        if not self._credentials:
            logger.info("Credentials are not provided")

            await raise_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message=constants.APIResponseMessageTemplate.UNAUTHORIZED,
            )

        if not await self._is_valid_token():
            logger.info("Token validation failed")

            await raise_http_exception(
                status_code=status.HTTP_403_FORBIDDEN,
                message=constants.APIResponseMessageTemplate.FORBIDDEN,
            )

    async def _is_valid_token(self) -> bool:
        """Validate token"""
        user = await get_current_user(token=self._credentials, request=self.request)
        return user is not None


class JWTTokenValidator:
    """Token validator class"""

    async def __call__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(jwt_scheme),
    ):
        _validator_service = JWTTokenValidatorService(
            credentials=credentials, request=request
        )
        await _validator_service.validate()
