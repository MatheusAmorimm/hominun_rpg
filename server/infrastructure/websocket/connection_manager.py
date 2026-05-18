import json
from dataclasses import dataclass, field

from fastapi import WebSocket

from server.domain.game_state.turn_state import TurnState
from server.domain.value_objects.ws_event_type import ServerEvent

MAX_PLAYERS_PER_SESSION = 4


@dataclass
class PlayerConnection:
    websocket: WebSocket
    user_id: str
    character_id: str
    nickname: str


class SessionRoom:
    def __init__(self) -> None:
        self.connections: list[PlayerConnection] = []
        self.turn_state = TurnState()

    def is_full(self) -> bool:
        return len(self.connections) >= MAX_PLAYERS_PER_SESSION

    def get_connection(self, user_id: str) -> PlayerConnection | None:
        return next((c for c in self.connections if c.user_id == user_id), None)

    def player_ids(self) -> list[str]:
        return [c.user_id for c in self.connections]


class ConnectionManager:
    def __init__(self) -> None:
        self._rooms: dict[str, SessionRoom] = {}

    def _room(self, session_id: str) -> SessionRoom:
        if session_id not in self._rooms:
            self._rooms[session_id] = SessionRoom()
        return self._rooms[session_id]

    def get_turn_state(self, session_id: str) -> TurnState:
        return self._room(session_id).turn_state

    def get_connection(self, session_id: str, user_id: str) -> PlayerConnection | None:
        return self._room(session_id).get_connection(user_id)

    async def connect(
        self,
        session_id: str,
        websocket: WebSocket,
        user_id: str,
        character_id: str,
        nickname: str,
    ) -> bool:
        room = self._room(session_id)
        if room.is_full():
            await websocket.close(code=4003, reason="Sessão cheia (máximo 4 jogadores).")
            return False

        await websocket.accept()
        conn = PlayerConnection(websocket, user_id, character_id, nickname)
        room.connections.append(conn)
        room.turn_state.add_player(user_id)

        await self.broadcast(session_id, {
            "event": ServerEvent.PLAYER_JOINED,
            "user_id": user_id,
            "nickname": nickname,
            "turn_order": room.turn_state.turn_order,
            "players": room.player_ids(),
        })
        return True

    async def disconnect(self, session_id: str, user_id: str) -> None:
        room = self._rooms.get(session_id)
        if not room:
            return

        conn = room.get_connection(user_id)
        if conn:
            room.connections.remove(conn)

        room.turn_state.remove_player(user_id)

        await self.broadcast(session_id, {
            "event": ServerEvent.PLAYER_LEFT,
            "user_id": user_id,
            "turn_order": room.turn_state.turn_order,
            "active_player_id": room.turn_state.active_player_id,
        })

        if not room.connections:
            del self._rooms[session_id]

    async def broadcast(self, session_id: str, payload: dict) -> None:
        room = self._rooms.get(session_id)
        if not room:
            return
        message = json.dumps(payload, default=str)
        for conn in list(room.connections):
            try:
                await conn.websocket.send_text(message)
            except Exception:
                pass

    async def send_to(self, session_id: str, user_id: str, payload: dict) -> None:
        conn = self._room(session_id).get_connection(user_id)
        if conn:
            try:
                await conn.websocket.send_text(json.dumps(payload, default=str))
            except Exception:
                pass

    async def send_error(self, session_id: str, user_id: str, detail: str) -> None:
        await self.send_to(session_id, user_id, {
            "event": ServerEvent.ERROR,
            "detail": detail,
        })


manager = ConnectionManager()
