from dataclasses import dataclass
from item_attributes import Item_Attribute
@dataclass
class Sub_Category_Item:
    name : str
    attributes : Item_Attribute