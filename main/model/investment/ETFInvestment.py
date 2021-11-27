from prompt_toolkit import print_formatted_text, HTML
from sharepp import SharePP

from main.model.investment.BaseInvestment import BaseInvestment


class ETFInvestment(BaseInvestment):
    investment_sum: float

    def __init__(self, isin: str, enabled: bool, name: str, quantity: float, allocation: float = 0.0):
        super().__init__(enabled, name, quantity, allocation)
        self.isin = isin

    def __eq__(self, other: object) -> bool:
        if other == self:
            return True
        if not isinstance(other, ETFInvestment):
            return False
        return other.isin == self.isin

    def __hash__(self) -> int:
        return self.isin.__hash__()

    def calculate_current_value(self):
        self.current_value = self.quantity * SharePP.get_etf_price(self.isin)

    def print(self):
        value_str = "{value:.2f}€"
        print_formatted_text(HTML(""))
        print_formatted_text(HTML("<b>" + self.name + "</b>"))
        print_formatted_text(HTML("ISIN: " + self.isin))
        print_formatted_text(HTML("Investment value: <u>" + value_str.format(value=self.investment_value) + "</u>"))
