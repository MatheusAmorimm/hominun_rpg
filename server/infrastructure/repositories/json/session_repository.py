from server.domain.game_state.session_state import SessionState
from server.domain.ports.session_repository import SessionRepository


class InMemorySessionRepository(SessionRepository):
    def __init__(self) -> None:
        self._store: dict[str, SessionState] = {}

    async def save(self, session: SessionState) -> None:
        self._store[session.session_id] = session

    async def get_by_id(self, session_id: str) -> SessionState | None:
        return self._store.get(session_id)
