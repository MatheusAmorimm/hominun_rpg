from server.domain.entities.region import Region
from server.domain.ports.region_repository import RegionRepository
from server.shared.exceptions import EntityNotFoundError


class GetRegionUseCase:
    def __init__(self, repo: RegionRepository) -> None:
        self._repo = repo

    async def execute(self, region_id: str) -> Region:
        region = await self._repo.get_by_id(region_id)
        if not region:
            raise EntityNotFoundError(f"Região '{region_id}' não encontrada.")
        return region
