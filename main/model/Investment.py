from functools import total_ordering

import sharepp
from main.model.Named import Named


@total_ordering
class Investment(Named):
    investment_sum: float

    def __init__(self, isin: str, name: str, quantity: float):
        super().__init__(name)
        self.isin = isin
        self.quantity = quantity
        self.current_value = quantity * sharepp.parse_price(isin)

    def __str__(self):
        result = self.isin
        result += "\n    Name: " + self.name
        value_str = "{value: .2f}€"
        result += "\n    Value: " + value_str.format(value=self.current_value)
        return result

    def __eq__(self, other: object) -> bool:
        if other == self:
            return True
        if not isinstance(other, Investment):
            return False
        return other.isin == self.isin

    def __hash__(self) -> int:
        return self.isin.__hash__()

    def __lt__(self, other) -> bool:
        return self.current_value > other.current_value
