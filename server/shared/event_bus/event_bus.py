from collections import defaultdict
from typing import Any, Callable


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def subscribe(self, event: str, handler: Callable[..., Any]) -> None:
        self._subscribers[event].append(handler)

    def publish(self, event: str, payload: Any = None) -> None:
        for handler in self._subscribers[event]:
            handler(payload)

    def unsubscribe(self, event: str, handler: Callable[..., Any]) -> None:
        self._subscribers[event].remove(handler)
