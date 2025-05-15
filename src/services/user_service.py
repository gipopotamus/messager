from src.repositories.user import UserRepository
from src.core.auth import create_access_token
from src.schemas.auth import Token


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def authenticate(self, username: str, password: str) -> Token:
        user = await self.repo.get_by_username(username)
        if not user or not user.password_hash == password:  # TODO: use password hasher
            raise ValueError("Invalid credentials")

        token = create_access_token(str(user.id))
        return Token(access_token=token)
