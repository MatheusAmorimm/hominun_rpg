from server.domain.game_state.session_state import SessionState
from server.domain.ports.region_repository import RegionRepository
from server.domain.ports.session_repository import SessionRepository
from server.shared.exceptions import EntityNotFoundError, InvalidActionError


class MovePlayerUseCase:
    def __init__(self, region_repo: RegionRepository, session_repo: SessionRepository) -> None:
        self._region_repo = region_repo
        self._session_repo = session_repo

    async def execute(self, session_id: str, region_id: str) -> SessionState:
        session = await self._session_repo.get_by_id(session_id)
        if not session:
            raise EntityNotFoundError(f"Sessão '{session_id}' não encontrada.")

        region = await self._region_repo.get_by_id(region_id)
        if not region:
            raise EntityNotFoundError(f"Região '{region_id}' não encontrada.")

        if not region.is_accessible_with_flags(session.narrative_flags):
            missing = [k for k, v in region.narrative_flags_required.items() if session.narrative_flags.get(k) != v]
            raise InvalidActionError(
                f"Região requer flags: {missing}",
            )

        session.current_region = region_id
        session.current_scene = ""
        await self._session_repo.save(session)
        return session
