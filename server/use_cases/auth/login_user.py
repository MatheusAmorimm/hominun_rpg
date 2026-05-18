from server.domain.entities.user import User
from server.domain.ports.user_repository import UserRepository
from server.infrastructure.auth.password_service import verify_password
from server.shared.exceptions import InvalidActionError


class LoginUserUseCase:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def execute(self, email: str, password: str) -> User:
        user = await self._repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidActionError("Email ou senha incorretos.")
        return user
