from fastapi import APIRouter, Depends, HTTPException, Query, status

from server.api.dependencies import get_get_domains_uc, get_unlock_node_uc
from server.api.middleware.auth import get_current_user
from server.api.schemas.progression import (
    ProgressionDomainResponse,
    ProgressionNodeResponse,
    UnlockNodeRequest,
    UnlockNodeResponse,
)
from server.shared.exceptions import EntityNotFoundError, InvalidActionError
from server.use_cases.progression.get_domains import GetProgressionDomainsUseCase
from server.use_cases.progression.unlock_node import UnlockNodeUseCase

router = APIRouter(prefix="/progression", tags=["progression"], dependencies=[Depends(get_current_user)])


@router.get("/domains", response_model=list[ProgressionDomainResponse])
async def get_domains(
    session_id: str = Query(...),
    archetype: str = Query(...),
    total_demon_level: int = Query(0, ge=0),
    uc: GetProgressionDomainsUseCase = Depends(get_get_domains_uc),
) -> list[ProgressionDomainResponse]:
    try:
        domains = await uc.execute(session_id, archetype, total_demon_level)
        return [
            ProgressionDomainResponse(
                id=d["id"],
                name=d["name"],
                primary_archetype=d["primary_archetype"],
                nodes=[ProgressionNodeResponse(**n) for n in d["nodes"]],
            )
            for d in domains
        ]
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/sessions/{session_id}/nodes/unlock", response_model=UnlockNodeResponse)
async def unlock_node(
    session_id: str,
    body: UnlockNodeRequest,
    archetype: str = Query(...),
    total_demon_level: int = Query(0, ge=0),
    uc: UnlockNodeUseCase = Depends(get_unlock_node_uc),
) -> UnlockNodeResponse:
    try:
        result = await uc.execute(session_id, body.node_id, archetype, total_demon_level)
        return UnlockNodeResponse(**result)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidActionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
