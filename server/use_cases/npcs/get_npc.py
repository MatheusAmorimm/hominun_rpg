from server.domain.entities.npc import Npc
from server.domain.ports.npc_repository import NpcRepository
from server.shared.exceptions import EntityNotFoundError


class GetNpcUseCase:
    def __init__(self, repo: NpcRepository) -> None:
        self._repo = repo

    async def execute(self, npc_id: str) -> Npc:
        npc = await self._repo.get_by_id(npc_id)
        if not npc:
            raise EntityNotFoundError(f"NPC '{npc_id}' não encontrado.")
        return npc
