from fastapi import APIRouter, Depends, HTTPException, Query, status

from server.api.dependencies import get_get_region_uc, get_get_regions_uc, get_move_player_uc
from server.api.middleware.auth import get_current_user
from server.api.schemas.region import (
    MovePlayerRequest,
    MovePlayerResponse,
    RegionResponse,
    RegionSummaryResponse,
)
from server.domain.entities.region import Region
from server.shared.exceptions import EntityNotFoundError, InvalidActionError
from server.use_cases.regions.get_region import GetRegionUseCase
from server.use_cases.regions.get_regions import GetRegionsUseCase
from server.use_cases.regions.move_player import MovePlayerUseCase

router = APIRouter(prefix="/regions", tags=["regions"], dependencies=[Depends(get_current_user)])


def _to_summary(r: Region) -> RegionSummaryResponse:
    return RegionSummaryResponse(
        id=r.id,
        name=r.name,
        type=r.type.value,
        danger_level=r.danger_level.value,
        available_in_acts=sorted(r.available_in_acts),
        connected_region_ids=list(r.connected_region_ids),
    )


def _to_full(r: Region) -> RegionResponse:
    return RegionResponse(
        id=r.id,
        name=r.name,
        type=r.type.value,
        danger_level=r.danger_level.value,
        requires_flags=r.narrative_flags_required,
        survival_item=r.survival_item_id() if r.requires_survival_item() else None,
        procedural=r.is_procedural(),
        special_properties=list(r.special_properties.keys()),
        lore=r.lore,
        connected_region_ids=list(r.connected_region_ids),
        available_in_acts=sorted(r.available_in_acts),
    )


@router.get("", response_model=list[RegionSummaryResponse])
async def list_regions(
    act: int | None = Query(None, ge=1, le=4),
    uc: GetRegionsUseCase = Depends(get_get_regions_uc),
) -> list[RegionSummaryResponse]:
    regions = await uc.execute(act=act)
    return [_to_summary(r) for r in regions]


@router.get("/{region_id}", response_model=RegionResponse)
async def get_region(
    region_id: str,
    uc: GetRegionUseCase = Depends(get_get_region_uc),
) -> RegionResponse:
    try:
        region = await uc.execute(region_id)
        return _to_full(region)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/sessions/{session_id}/move", response_model=MovePlayerResponse)
async def move_player(
    session_id: str,
    body: MovePlayerRequest,
    uc: MovePlayerUseCase = Depends(get_move_player_uc),
) -> MovePlayerResponse:
    try:
        session = await uc.execute(session_id=session_id, region_id=body.region_id)
        return MovePlayerResponse(
            session_id=session.session_id,
            current_region=session.current_region,
            current_scene=session.current_scene,
        )
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidActionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
