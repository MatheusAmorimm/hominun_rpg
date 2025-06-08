from dataclasses import dataclass
from category_item import Category

@dataclass
class Item:
    name : str
    category: Category