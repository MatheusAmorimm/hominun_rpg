from server.domain.game_state.session_state import SessionState
from server.domain.ports.session_repository import SessionRepository
from server.shared.exceptions import EntityNotFoundError


class GetSessionUseCase:
    def __init__(self, repo: SessionRepository) -> None:
        self._repo = repo

    async def execute(self, session_id: str) -> SessionState:
        session = await self._repo.get_by_id(session_id)
        if not session:
            raise EntityNotFoundError(f"Sessão '{session_id}' não encontrada.")
        return session
