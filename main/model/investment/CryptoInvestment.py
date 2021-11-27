from prompt_toolkit import print_formatted_text, HTML
from sharepp import SharePP, Coin

from main.model.investment.BaseInvestment import BaseInvestment


class CryptoInvestment(BaseInvestment):
    def __init__(self, coin: Coin, enabled: bool, name: str, quantity: float, allocation: float = 0.0):
        super().__init__(enabled, name, quantity, allocation)
        self.coin = coin

    def __eq__(self, other: object) -> bool:
        if other == self:
            return True
        if not isinstance(other, CryptoInvestment):
            return False
        return other.coin == self.coin

    def __hash__(self) -> int:
        return self.coin.__hash__()

    def calculate_current_value(self):
        self.current_value = self.quantity * SharePP.get_coin_price(self.coin)

    def print(self):
        value_str = "{value:.2f}€"
        print_formatted_text(HTML(""))
        print_formatted_text(HTML("<b>" + self.name + "</b>"))
        print_formatted_text(HTML("Investment value: <u>" + value_str.format(value=self.investment_value) + "</u>"))
