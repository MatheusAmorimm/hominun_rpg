import json

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from server.api.schemas.ws import ClientMessage
from server.infrastructure.auth.jwt_service import decode_access_token
from server.infrastructure.database.base import AsyncSessionFactory
from server.infrastructure.repositories.json.region_repository import JsonRegionRepository
from server.infrastructure.repositories.postgres.session_repository import PostgresSessionRepository
from server.infrastructure.websocket.connection_manager import manager
from server.shared.exceptions import InvalidActionError
from server.use_cases.multiplayer.handle_player_action import HandlePlayerActionUseCase
from server.infrastructure.repositories.postgres.user_repository import PostgresUserRepository
from server.domain.value_objects.ws_event_type import ServerEvent

router = APIRouter(prefix="/ws", tags=["websocket"])

_region_repo = JsonRegionRepository()


@router.websocket("/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    token: str = Query(...),
) -> None:
    # Auth via query param token
    try:
        user_id = decode_access_token(token)
    except InvalidActionError:
        await websocket.close(code=4001, reason="Token inválido ou expirado.")
        return

    async with AsyncSessionFactory() as db:
        user_repo = PostgresUserRepository(db)
        user = await user_repo.get_by_id(user_id)
        if not user:
            await websocket.close(code=4001, reason="Usuário não encontrado.")
            return

        session_repo = PostgresSessionRepository(db)
        session = await session_repo.get_by_id(session_id)
        if not session:
            await websocket.close(code=4004, reason="Sessão não encontrada.")
            return

    user_id_str = str(user_id)
    connected = await manager.connect(
        session_id=session_id,
        websocket=websocket,
        user_id=user_id_str,
        character_id=session.player_id,
        nickname=user.nickname,
    )
    if not connected:
        return

    # Send initial state to the joining player
    turn_state = manager.get_turn_state(session_id)
    await manager.send_to(session_id, user_id_str, {
        "event": ServerEvent.STATE_UPDATE,
        "session": {
            "session_id": session.session_id,
            "current_region": session.current_region,
            "faction_reputations": session.faction_reputations,
            "unlocked_nodes": session.unlocked_nodes,
            "completed_milestones": session.completed_milestones,
        },
        "turn": {
            "active_player_id": turn_state.active_player_id,
            "turn_number": turn_state.turn_number,
            "turn_order": turn_state.turn_order,
        },
    })

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
                msg = ClientMessage.model_validate(data)
            except Exception:
                await manager.send_error(session_id, user_id_str, "Mensagem inválida.")
                continue

            async with AsyncSessionFactory() as db:
                session_repo = PostgresSessionRepository(db)
                use_case = HandlePlayerActionUseCase(session_repo, _region_repo, manager)
                await use_case.execute(session_id, user_id_str, msg.event, msg.payload)

    except WebSocketDisconnect:
        await manager.disconnect(session_id, user_id_str)
