from dataclasses import dataclass


@dataclass(frozen=True)
class BaseStats:
    str_: int  # Força
    dex: int   # Destreza
    con: int   # Constituição
    int_: int  # Inteligência
    wis: int   # Sabedoria
    cha: int   # Carisma

    @staticmethod
    def modifier(value: int) -> int:
        return (value - 10) // 2

    @property
    def str_mod(self) -> int:
        return self.modifier(self.str_)

    @property
    def dex_mod(self) -> int:
        return self.modifier(self.dex)

    @property
    def con_mod(self) -> int:
        return self.modifier(self.con)

    @property
    def int_mod(self) -> int:
        return self.modifier(self.int_)

    @property
    def wis_mod(self) -> int:
        return self.modifier(self.wis)

    @property
    def cha_mod(self) -> int:
        return self.modifier(self.cha)


@dataclass(frozen=True)
class DerivedStats:
    hp: int
    mana: int
    initiative: int
    ether_resistance: int

    @classmethod
    def from_base(
        cls,
        base: BaseStats,
        hp_bonus: int = 0,
        mana_bonus: int = 0,
    ) -> "DerivedStats":
        return cls(
            hp=50 + (base.con * 5) + hp_bonus,
            mana=30 + (base.int_ * 5) + mana_bonus,
            initiative=BaseStats.modifier(base.dex),
            ether_resistance=BaseStats.modifier(base.con) + BaseStats.modifier(base.wis),
        )
