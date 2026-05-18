from datetime import datetime, timezone
from uuid import uuid4

from server.domain.entities.user import User
from server.domain.ports.user_repository import UserRepository
from server.infrastructure.auth.password_service import hash_password
from server.shared.exceptions import InvalidActionError


class RegisterUserUseCase:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def execute(self, email: str, password: str, nickname: str) -> User:
        existing = await self._repo.get_by_email(email)
        if existing:
            raise InvalidActionError("Email já cadastrado.")

        now = datetime.now(timezone.utc)
        user = User(
            id=uuid4(),
            email=email,
            password_hash=hash_password(password),
            nickname=nickname,
            created_at=now,
            updated_at=now,
        )
        await self._repo.save(user)
        return user
