from server.domain.entities.npc import Npc
from server.domain.ports.npc_repository import NpcRepository


class GetNpcsUseCase:
    def __init__(self, repo: NpcRepository) -> None:
        self._repo = repo

    async def execute(self, region_id: str | None = None, act: int | None = None) -> list[Npc]:
        if region_id:
            npcs = await self._repo.get_by_region(region_id)
        else:
            npcs = await self._repo.get_all()

        if act is not None:
            npcs = [n for n in npcs if n.is_available_in_act(act)]

        return npcs
