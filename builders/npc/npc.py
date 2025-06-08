from dataclasses import dataclass
from ancestries import Ancestries
from _classes import _Classes

@dataclass
class NPC:
    name : str
    ancestries : Ancestries
    class_ : _Classes
