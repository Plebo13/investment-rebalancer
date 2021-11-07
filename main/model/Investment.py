from functools import total_ordering
from main.model.Named import Named
from typing import List
import sharepp


@total_ordering
class Investment(Named):
    investment_sum: float

    def __init__(self, isin: str, name: str, quantity: float):
        super().__init__(name)
        self.isin = isin
        self.quantity = quantity
        self.current_value = quantity * sharepp.parse_price(isin)
        self.categories: List[str] = []

    def __str__(self):
        return self.name

    def __eq__(self, other: object) -> bool:
        if other == self:
            return True
        if not isinstance(other, Investment):
            return False
        return other.isin == self.isin

    def __lt__(self, other) -> bool:
        return self.current_value > other.current_value

    def add_categories(self, categories_str: str):
        for category_str in categories_str.split(","):
            self.add_category(category_str)

    def add_category(self, category_str: str):
        self.categories.append(category_str)
