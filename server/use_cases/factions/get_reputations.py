from server.domain.entities.faction import Faction
from server.domain.ports.faction_repository import FactionRepository
from server.domain.ports.session_repository import SessionRepository
from server.shared.exceptions import EntityNotFoundError


class GetReputationsUseCase:
    def __init__(self, faction_repo: FactionRepository, session_repo: SessionRepository) -> None:
        self._faction_repo = faction_repo
        self._session_repo = session_repo

    async def execute(self, session_id: str) -> dict[str, dict]:
        session = await self._session_repo.get_by_id(session_id)
        if not session:
            raise EntityNotFoundError(f"Sessão '{session_id}' não encontrada.")

        factions: list[Faction] = await self._faction_repo.get_all()
        faction_map = {f.id: f for f in factions}

        result = {}
        for faction_id, score in session.faction_reputations.items():
            faction = faction_map.get(faction_id)
            status = faction.reputation_status(score).value if faction else "unknown"
            result[faction_id] = {"score": score, "status": status}

        return result
