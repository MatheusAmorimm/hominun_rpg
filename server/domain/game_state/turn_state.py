from dataclasses import dataclass, field


@dataclass
class TurnState:
    turn_order: list[str] = field(default_factory=list)  # list of user_ids
    current_player_idx: int = 0
    turn_number: int = 1

    @property
    def active_player_id(self) -> str | None:
        if not self.turn_order:
            return None
        return self.turn_order[self.current_player_idx % len(self.turn_order)]

    def advance(self) -> str | None:
        if not self.turn_order:
            return None
        self.current_player_idx = (self.current_player_idx + 1) % len(self.turn_order)
        if self.current_player_idx == 0:
            self.turn_number += 1
        return self.active_player_id

    def add_player(self, user_id: str) -> None:
        if user_id not in self.turn_order:
            self.turn_order.append(user_id)

    def remove_player(self, user_id: str) -> None:
        if user_id not in self.turn_order:
            return
        idx = self.turn_order.index(user_id)
        self.turn_order.remove(user_id)
        if not self.turn_order:
            self.current_player_idx = 0
            return
        if idx < self.current_player_idx:
            self.current_player_idx -= 1
        self.current_player_idx %= len(self.turn_order)

    def is_active(self, user_id: str) -> bool:
        return self.active_player_id == user_id
