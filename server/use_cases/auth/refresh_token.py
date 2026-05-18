from server.domain.entities.user import User
from server.domain.ports.user_repository import UserRepository
from server.infrastructure.auth.jwt_service import decode_refresh_token
from server.shared.exceptions import EntityNotFoundError, InvalidActionError


class RefreshTokenUseCase:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def execute(self, refresh_token: str) -> User:
        user_id = decode_refresh_token(refresh_token)
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError("Usuário não encontrado.")
        return user
