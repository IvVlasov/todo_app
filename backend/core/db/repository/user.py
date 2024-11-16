from backend.api.v1.auth.models import TokenPayload
from backend.core.db.repository.base import BaseRepository
from backend.core.models import User, UserCreate


class UserRepository(BaseRepository):
    """User repository"""

    async def create_user(self, user: UserCreate) -> int | None:
        """Create user"""
        query = """
            INSERT INTO users (email, password)
            VALUES ($1, $2)
            RETURNING user_id
        """
        user_id = await self.connector.get_query_result_as_dict(
            query, user.email, user.password
        )
        if not user_id:
            return None
        return user_id.get("user_id")

    async def get_user_by_credentials(self, email: str, password: str) -> User | None:
        """Get user by credentials"""
        query = """
            SELECT * FROM users WHERE email = $1 AND password = $2
        """
        result = await self.connector.get_query_result_as_dict(query, email, password)
        return User(**result) if result else None

    async def get_user_by_token_payload(
        self, token_payload: TokenPayload
    ) -> User | None:
        """Get user by token payload"""
        query = """
            SELECT * FROM users WHERE user_id = $1 AND email = $2
        """
        result = await self.connector.get_query_result_as_dict(
            query, token_payload.user_id, token_payload.email
        )
        return User(**result) if result else None
