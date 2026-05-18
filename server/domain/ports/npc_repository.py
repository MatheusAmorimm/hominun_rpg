from abc import ABC, abstractmethod

from server.domain.entities.npc import Npc


class NpcRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Npc]: ...

    @abstractmethod
    async def get_by_id(self, npc_id: str) -> Npc | None: ...

    @abstractmethod
    async def get_by_region(self, region_id: str) -> list[Npc]: ...
