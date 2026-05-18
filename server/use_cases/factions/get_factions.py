from server.domain.entities.faction import Faction
from server.domain.ports.faction_repository import FactionRepository


class GetFactionsUseCase:
    def __init__(self, repo: FactionRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[Faction]:
        return await self._repo.get_all()
