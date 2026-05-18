from abc import ABC, abstractmethod

from server.domain.game_state.session_state import SessionState


class SessionRepository(ABC):
    @abstractmethod
    async def save(self, session: SessionState) -> None: ...

    @abstractmethod
    async def get_by_id(self, session_id: str) -> SessionState | None: ...
