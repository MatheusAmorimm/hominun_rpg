from server.domain.entities.region import Region
from server.domain.ports.region_repository import RegionRepository


class GetRegionsUseCase:
    def __init__(self, repo: RegionRepository) -> None:
        self._repo = repo

    async def execute(self, act: int | None = None) -> list[Region]:
        regions = await self._repo.get_all()
        if act is not None:
            regions = [r for r in regions if r.is_accessible_in_act(act)]
        return regions
