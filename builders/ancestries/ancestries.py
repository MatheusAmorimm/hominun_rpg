from dataclasses import dataclass
from ancestries_attributes import Ancestries_Attributes

@dataclass
class Ancestries:
    name : str
    gender : str
    base_hp : int
    base_damage : int
    base_mana : int
    base_armor : int
    atributes : Ancestries_Attributes
