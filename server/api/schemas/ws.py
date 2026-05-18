from typing import Any

from pydantic import BaseModel

from server.domain.value_objects.ws_event_type import ClientEvent


class ClientMessage(BaseModel):
    event: ClientEvent
    payload: dict[str, Any] = {}


class MovePayload(BaseModel):
    region_id: str


class ChoicePayload(BaseModel):
    choice_id: str
    context: dict[str, Any] = {}


class CombatPayload(BaseModel):
    action_type: str
    target_id: str | None = None


class ChatPayload(BaseModel):
    message: str
