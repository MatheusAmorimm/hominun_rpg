from uuid import UUID, uuid4

from server.domain.game_state.session_state import SessionState
from server.domain.ports.character_repository import CharacterRepository
from server.domain.ports.session_repository import SessionRepository
from server.shared.exceptions import EntityNotFoundError, InvalidActionError


class CreateSessionUseCase:
    def __init__(self, session_repo: SessionRepository, character_repo: CharacterRepository) -> None:
        self._session_repo = session_repo
        self._character_repo = character_repo

    async def execute(self, user_id: UUID, character_id: UUID) -> SessionState:
        character = await self._character_repo.get_by_id(character_id)
        if not character:
            raise EntityNotFoundError("Personagem não encontrado.")
        if character.user_id != user_id:
            raise InvalidActionError("Este personagem não pertence ao usuário autenticado.")

        session = SessionState(
            session_id=str(uuid4()),
            player_id=str(character_id),
        )
        await self._session_repo.save(session)
        return session
