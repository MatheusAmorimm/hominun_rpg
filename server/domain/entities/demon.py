from dataclasses import dataclass
from uuid import UUID

from server.domain.value_objects.demon_type import DemonTemperament


@dataclass
class Demon:
    id: UUID
    species_id: str
    owner_player_id: UUID
    given_name: str
    temperament: DemonTemperament
    affinity: int
    current_hp: int
    current_mana: int
    level: int
    is_active: bool

    # Comunicação é mental — o demônio NÃO fala.
    # A afinidade determina a qualidade do vínculo mental.

    MAX_AFFINITY = 100

    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0

    def gain_affinity(self, amount: int) -> int:
        previous = self.affinity
        self.affinity = min(self.MAX_AFFINITY, self.affinity + amount)
        return self.affinity - previous

    def lose_affinity(self, amount: int) -> None:
        self.affinity = max(0, self.affinity - amount)

    def take_damage(self, amount: int) -> None:
        self.current_hp = max(0, self.current_hp - amount)

    def spend_mana(self, amount: int) -> bool:
        if self.current_mana < amount:
            return False
        self.current_mana -= amount
        return True

    @property
    def affinity_tier(self) -> str:
        if self.affinity >= 80:
            return "sincronizado"
        if self.affinity >= 50:
            return "vinculado"
        if self.affinity >= 20:
            return "receptivo"
        return "resistente"
