from prompt_toolkit import print_formatted_text, HTML
from sharepp import SharePP

from investment_rebalancer.model.investment.BaseInvestment import BaseInvestment


class ETFInvestment(BaseInvestment):
    investment_sum: float

    def __init__(self, isin: str, enabled: bool, name: str, quantity: float, target_allocation: float = 0.0):
        """
        Constructor for a given isin, name, quantity, enabled flag and optional allocation.
        :param isin: the investments isin
        :param enabled: flag whether this investment is enabled or not
        :param name: the investments name
        :param quantity: the investments quantity
        :param target_allocation: the investments allocation
        """
        super().__init__(enabled, name, quantity, target_allocation)
        self.isin = isin

    def __eq__(self, other: object) -> bool:
        """
        Checks whether or not an object is equal to this instance.
        Two etf investments are equal if they have the same isin.
        :param other: the other object
        :return: true if the other object is equal, otherwise false
        """
        if other == self:
            return True
        if not isinstance(other, ETFInvestment):
            return False
        return other.isin == self.isin

    def __hash__(self) -> int:
        """
        Calculates the hash of this instance.
        :return: the hash
        """
        return self.isin.__hash__()

    def calculate_current_value(self):
        self.current_value = self.quantity * SharePP.get_etf_price(self.isin)

    def print(self):
        value_str = "{value:.2f}€"
        print_formatted_text(HTML(""))
        print_formatted_text(HTML("<b>" + self.name + "</b>"))
        print_formatted_text(HTML("ISIN: " + self.isin))
        print_formatted_text(HTML("Investment value: <u>" + value_str.format(value=self.investment_value) + "</u>"))
