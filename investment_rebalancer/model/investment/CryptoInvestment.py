from prompt_toolkit import print_formatted_text, HTML
from sharepp import SharePP, Coin

from investment_rebalancer.model.investment.BaseInvestment import BaseInvestment


class CryptoInvestment(BaseInvestment):
    def __init__(self, coin: Coin, enabled: bool, name: str, quantity: float, target_allocation: float = 0.0):
        """
        Constructor for a given coin, name, quantity, enabled flag and optional allocation.
        :param coin: the coin that this investment is representing
        :param enabled: flag whether this investment is enabled or not
        :param name: the investments name
        :param quantity: the investments quantity
        :param target_allocation: the investments allocation
        """
        super().__init__(enabled, name, quantity, target_allocation)
        self.coin = coin

    def __eq__(self, other: object) -> bool:
        """
        Checks whether or not an object is equal to this instance.
        Two coins are equal if they represent the same coin.
        :param other: the other object
        :return: true if the other object is equal, otherwise false
        """
        if other == self:
            return True
        if not isinstance(other, CryptoInvestment):
            return False
        return other.coin == self.coin

    def __hash__(self) -> int:
        """
        Calculates the hash of this instance.
        :return: the hash
        """
        return self.coin.__hash__()

    def calculate_current_value(self):
        self.current_value = self.quantity * SharePP.get_coin_price(self.coin)

    def print(self):
        value_str = "{value:.2f}€"
        print_formatted_text(HTML(""))
        print_formatted_text(HTML("<b>" + self.name + "</b>"))
        print_formatted_text(HTML("Investment value: <u>" + value_str.format(value=self.investment_value) + "</u>"))
