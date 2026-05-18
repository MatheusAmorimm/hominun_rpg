from server.domain.ports.faction_repository import FactionRepository
from server.domain.ports.session_repository import SessionRepository
from server.shared.exceptions import EntityNotFoundError


class UpdateReputationUseCase:
    def __init__(self, faction_repo: FactionRepository, session_repo: SessionRepository) -> None:
        self._faction_repo = faction_repo
        self._session_repo = session_repo

    async def execute(self, session_id: str, faction_id: str, delta: int) -> dict:
        session = await self._session_repo.get_by_id(session_id)
        if not session:
            raise EntityNotFoundError(f"Sessão '{session_id}' não encontrada.")

        faction = await self._faction_repo.get_by_id(faction_id)
        if not faction:
            raise EntityNotFoundError(f"Facção '{faction_id}' não encontrada.")

        current = session.faction_reputations.get(faction_id, 0)
        new_score = max(-100, min(100, current + delta))
        session.faction_reputations[faction_id] = new_score

        await self._session_repo.save(session)

        return {
            "faction_id": faction_id,
            "score": new_score,
            "status": faction.reputation_status(new_score).value,
        }
