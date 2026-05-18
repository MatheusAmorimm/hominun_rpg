from abc import ABC, abstractmethod

from server.domain.entities.region import Region


class RegionRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Region]: ...

    @abstractmethod
    async def get_by_id(self, region_id: str) -> Region | None: ...
