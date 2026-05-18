from typing import Any


class FlagRegistry:
    def __init__(self, initial: dict[str, Any] | None = None) -> None:
        self._flags: dict[str, Any] = initial or {}

    def set(self, key: str, value: Any) -> None:
        self._flags[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._flags.get(key, default)

    def snapshot(self) -> dict[str, Any]:
        return dict(self._flags)
