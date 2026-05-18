from fastapi import APIRouter, Depends, HTTPException, Query, status

from server.api.dependencies import get_get_npc_uc, get_get_npcs_uc
from server.api.middleware.auth import get_current_user
from server.api.schemas.npc import NpcResponse, NpcSummaryResponse
from server.domain.entities.npc import Npc
from server.shared.exceptions import EntityNotFoundError
from server.use_cases.npcs.get_npc import GetNpcUseCase
from server.use_cases.npcs.get_npcs import GetNpcsUseCase

router = APIRouter(prefix="/npcs", tags=["npcs"], dependencies=[Depends(get_current_user)])


def _to_summary(n: Npc) -> NpcSummaryResponse:
    return NpcSummaryResponse(
        id=n.id,
        name=n.name,
        full_name=n.full_name,
        race=n.race.value,
        roles=[r.value for r in n.roles],
        alignment=n.alignment.value,
        status=n.status.value,
        is_rival=n.is_rival,
    )


def _to_full(n: Npc) -> NpcResponse:
    return NpcResponse(
        id=n.id,
        name=n.name,
        full_name=n.full_name,
        title=n.title,
        race=n.race.value,
        roles=[r.value for r in n.roles],
        alignment=n.alignment.value,
        status=n.status.value,
        is_rival=n.is_rival,
        family_id=n.family_id,
        faction_ids=list(n.faction_ids),
        region_ids=list(n.region_ids),
        available_in_acts=sorted(n.available_in_acts),
        lore=n.lore,
        narrative_flags=n.narrative_flags,
    )


@router.get("", response_model=list[NpcSummaryResponse])
async def list_npcs(
    region_id: str | None = Query(None),
    act: int | None = Query(None, ge=1, le=4),
    uc: GetNpcsUseCase = Depends(get_get_npcs_uc),
) -> list[NpcSummaryResponse]:
    npcs = await uc.execute(region_id=region_id, act=act)
    return [_to_summary(n) for n in npcs]


@router.get("/{npc_id}", response_model=NpcResponse)
async def get_npc(
    npc_id: str,
    uc: GetNpcUseCase = Depends(get_get_npc_uc),
) -> NpcResponse:
    try:
        npc = await uc.execute(npc_id)
        return _to_full(npc)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
