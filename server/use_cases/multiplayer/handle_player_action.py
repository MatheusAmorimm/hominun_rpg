from server.domain.ports.region_repository import RegionRepository
from server.domain.ports.session_repository import SessionRepository
from server.domain.value_objects.ws_event_type import ClientEvent, ServerEvent
from server.infrastructure.websocket.connection_manager import ConnectionManager
from server.shared.exceptions import EntityNotFoundError, InvalidActionError


class HandlePlayerActionUseCase:
    def __init__(
        self,
        session_repo: SessionRepository,
        region_repo: RegionRepository,
        manager: ConnectionManager,
    ) -> None:
        self._session_repo = session_repo
        self._region_repo = region_repo
        self._manager = manager

    async def execute(
        self,
        session_id: str,
        user_id: str,
        event: ClientEvent,
        payload: dict,
    ) -> None:
        turn_state = self._manager.get_turn_state(session_id)

        if event == ClientEvent.CHAT:
            conn = self._manager.get_connection(session_id, user_id)
            nickname = conn.nickname if conn else user_id
            await self._manager.broadcast(session_id, {
                "event": ServerEvent.CHAT,
                "user_id": user_id,
                "nickname": nickname,
                "message": payload.get("message", ""),
            })
            return

        if not turn_state.is_active(user_id):
            await self._manager.send_error(
                session_id, user_id,
                f"Não é seu turno. Turno atual: {turn_state.active_player_id}",
            )
            return

        if event == ClientEvent.ACTION_MOVE:
            await self._handle_move(session_id, user_id, payload)

        elif event == ClientEvent.ACTION_CHOICE:
            await self._handle_choice(session_id, user_id, payload)

        elif event == ClientEvent.ACTION_COMBAT:
            await self._handle_combat(session_id, user_id, payload)

        elif event == ClientEvent.ACTION_END_TURN:
            await self._advance_turn(session_id, user_id)

    async def _handle_move(self, session_id: str, user_id: str, payload: dict) -> None:
        region_id = payload.get("region_id", "")
        try:
            session = await self._session_repo.get_by_id(session_id)
            if not session:
                raise EntityNotFoundError("Sessão não encontrada.")

            region = await self._region_repo.get_by_id(region_id)
            if not region:
                raise EntityNotFoundError(f"Região '{region_id}' não encontrada.")

            if not region.is_accessible_with_flags(session.narrative_flags):
                missing = [k for k, v in region.narrative_flags_required.items()
                           if session.narrative_flags.get(k) != v]
                raise InvalidActionError(f"Região requer flags: {missing}")

            session.current_region = region_id
            session.current_scene = ""
            await self._session_repo.save(session)

            await self._manager.broadcast(session_id, {
                "event": ServerEvent.PLAYER_ACTION,
                "action": "move",
                "user_id": user_id,
                "region_id": region_id,
                "region_name": region.name,
            })
            await self._advance_turn(session_id, user_id)

        except (EntityNotFoundError, InvalidActionError) as e:
            await self._manager.send_error(session_id, user_id, str(e))

    async def _handle_choice(self, session_id: str, user_id: str, payload: dict) -> None:
        choice_id = payload.get("choice_id", "")
        await self._manager.broadcast(session_id, {
            "event": ServerEvent.PLAYER_ACTION,
            "action": "choice",
            "user_id": user_id,
            "choice_id": choice_id,
            "context": payload.get("context", {}),
        })
        await self._advance_turn(session_id, user_id)

    async def _handle_combat(self, session_id: str, user_id: str, payload: dict) -> None:
        await self._manager.broadcast(session_id, {
            "event": ServerEvent.PLAYER_ACTION,
            "action": "combat",
            "user_id": user_id,
            "action_type": payload.get("action_type"),
            "target_id": payload.get("target_id"),
        })
        await self._advance_turn(session_id, user_id)

    async def _advance_turn(self, session_id: str, user_id: str) -> None:
        turn_state = self._manager.get_turn_state(session_id)
        next_player = turn_state.advance()
        await self._manager.broadcast(session_id, {
            "event": ServerEvent.TURN_START,
            "active_player_id": next_player,
            "turn_number": turn_state.turn_number,
        })
