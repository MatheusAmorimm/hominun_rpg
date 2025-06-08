from dataclasses import dataclass
from ancestries import Ancestrie
from _classes import _Classes

@dataclass
class Char:
    name : str
    ancestrie : Ancestrie
    class_ : _Classes