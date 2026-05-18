from abc import ABC, abstractmethod

from server.domain.entities.progression import ProgressionDomain


class ProgressionRepository(ABC):
    @abstractmethod
    async def get_all_domains(self) -> list[ProgressionDomain]: ...

    @abstractmethod
    async def get_domain_by_id(self, domain_id: str) -> ProgressionDomain | None: ...

    @abstractmethod
    async def get_node_domain(self, node_id: str) -> ProgressionDomain | None: ...
