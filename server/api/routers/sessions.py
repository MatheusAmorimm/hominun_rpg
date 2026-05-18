from fastapi import APIRouter, Depends, HTTPException, status

from server.api.dependencies import get_create_session_uc, get_get_session_uc
from server.api.middleware.auth import get_current_user
from server.api.schemas.session import CreateSessionRequest, SessionResponse
from server.domain.entities.user import User
from server.domain.game_state.session_state import SessionState
from server.shared.exceptions import EntityNotFoundError, InvalidActionError
from server.use_cases.sessions.create_session import CreateSessionUseCase
from server.use_cases.sessions.get_session import GetSessionUseCase

router = APIRouter(prefix="/sessions", tags=["sessions"])


def _to_response(s: SessionState) -> SessionResponse:
    return SessionResponse(
        session_id=s.session_id,
        player_id=s.player_id,
        current_region=s.current_region,
        current_scene=s.current_scene,
        faction_reputations=s.faction_reputations,
        unlocked_nodes=s.unlocked_nodes,
        completed_milestones=s.completed_milestones,
        save_version=s.save_version,
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SessionResponse)
async def create_session(
    body: CreateSessionRequest,
    current_user: User = Depends(get_current_user),
    uc: CreateSessionUseCase = Depends(get_create_session_uc),
) -> SessionResponse:
    try:
        session = await uc.execute(user_id=current_user.id, character_id=body.character_id)
        return _to_response(session)
    except (EntityNotFoundError, InvalidActionError) as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    _: User = Depends(get_current_user),
    uc: GetSessionUseCase = Depends(get_get_session_uc),
) -> SessionResponse:
    try:
        session = await uc.execute(session_id)
        return _to_response(session)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
