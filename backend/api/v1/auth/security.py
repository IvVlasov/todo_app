# noinspection PyPackageRequirements
import logging

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.api.v1.auth.services.jwt_token import decode_jwt


logger = logging.getLogger(__name__)

oauth2_scheme = HTTPBearer(auto_error=False)


class JWTBearer(HTTPBearer):
    """JWT bearer"""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(
            request
        )
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials
        raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        """Verify JWT"""
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except Exception as error:
            logger.error("Error decoding JWT token: %s", error)
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


jwt_scheme = JWTBearer()
