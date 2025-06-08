from dataclasses import dataclass
from sub_category_item import Sub_Category_Item

@dataclass
class Category:
    name : str
    sub_cat : Sub_Category_Item