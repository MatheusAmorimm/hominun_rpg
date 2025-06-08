from dataclasses import dataclass
from expertise import Expertise

@dataclass
class _Classes:
    name : str
    attribute : Expertise
    base_hp : int
    base_mana : int
    base_armor : int