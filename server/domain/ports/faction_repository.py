from abc import ABC, abstractmethod

from server.domain.entities.faction import Faction


class FactionRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Faction]: ...

    @abstractmethod
    async def get_by_id(self, faction_id: str) -> Faction | None: ...
