from main.model.investment.ETFInvestment import ETFInvestment


class TERInvestment(ETFInvestment):

    def __init__(self, isin: str, enabled: bool, name: str, quantity: float, ter: float):
        """
        Constructor for a given isin, name, quantity, ter, enabled flag and optional allocation.
        :param isin: the investments isin
        :param enabled: flag whether this investment is enabled or not
        :param name: the investments name
        :param quantity: the investments quantity
        :param ter: the ter of this investment
        """
        super().__init__(isin, enabled, name, quantity)
        self.ter = ter

    def __lt__(self, other) -> bool:
        return self.ter > other.ter
