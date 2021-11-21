from functools import total_ordering

import sharepp
from prompt_toolkit import print_formatted_text, HTML

from main.model.Named import Named


@total_ordering
class Investment(Named):
    investment_sum: float

    def __init__(self, isin: str, enabled: bool, name: str, quantity: float):
        super().__init__(name)
        self.isin = isin
        self.enabled = enabled
        self.quantity = quantity
        self.current_value = 0.0
        self.investment_value = 0.0

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

    def calculate_current_value(self):
        self.current_value = self.quantity * sharepp.parse_price(self.isin)

    def print(self):
        value_str = "{value:.2f}€"
        print_formatted_text(HTML(""))
        print_formatted_text(HTML("<b>" + self.name + "</b>"))
        print_formatted_text(HTML("ISIN: " + self.isin))
        print_formatted_text(HTML("Current value: " + value_str.format(value=self.current_value)))
        print_formatted_text(HTML("Investment value: <u>" + value_str.format(value=self.investment_value) + "</u>"))
