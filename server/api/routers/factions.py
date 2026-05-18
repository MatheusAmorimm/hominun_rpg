from fastapi import APIRouter, Depends, HTTPException, status

from server.api.middleware.auth import get_current_user
from server.api.dependencies import (
    get_get_factions_uc,
    get_get_reputations_uc,
    get_update_reputation_uc,
)
from server.api.schemas.faction import (
    FactionSummaryResponse,
    ReputationEntry,
    ReputationsResponse,
    UpdateReputationRequest,
    UpdateReputationResponse,
)
from server.domain.entities.faction import Faction
from server.shared.exceptions import EntityNotFoundError, InvalidActionError
from server.use_cases.factions.get_factions import GetFactionsUseCase
from server.use_cases.factions.get_reputations import GetReputationsUseCase
from server.use_cases.factions.update_reputation import UpdateReputationUseCase

router = APIRouter(prefix="/factions", tags=["factions"], dependencies=[Depends(get_current_user)])


def _to_summary(f: Faction) -> FactionSummaryResponse:
    return FactionSummaryResponse(
        id=f.id,
        name=f.name,
        type=f.type.value,
        alignment=f.alignment.value,
        leader_npc_id=f.leader_npc_id,
        available_in_acts=sorted(f.available_in_acts),
    )


@router.get("", response_model=list[FactionSummaryResponse])
async def list_factions(
    uc: GetFactionsUseCase = Depends(get_get_factions_uc),
) -> list[FactionSummaryResponse]:
    factions = await uc.execute()
    return [_to_summary(f) for f in factions]


@router.get("/sessions/{session_id}/reputations", response_model=ReputationsResponse)
async def get_reputations(
    session_id: str,
    uc: GetReputationsUseCase = Depends(get_get_reputations_uc),
) -> ReputationsResponse:
    try:
        raw = await uc.execute(session_id)
        return ReputationsResponse(
            reputations={k: ReputationEntry(**v) for k, v in raw.items()}
        )
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/sessions/{session_id}/reputations/update", response_model=UpdateReputationResponse)
async def update_reputation(
    session_id: str,
    body: UpdateReputationRequest,
    uc: UpdateReputationUseCase = Depends(get_update_reputation_uc),
) -> UpdateReputationResponse:
    try:
        result = await uc.execute(session_id, body.faction_id, body.delta)
        return UpdateReputationResponse(**result)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidActionError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
