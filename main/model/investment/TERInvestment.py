from main.model.investment.ETFInvestment import ETFInvestment


class TERInvestment(ETFInvestment):

    def __init__(self, isin: str, enabled: bool, name: str, quantity: float, ter: float):
        super().__init__(isin, enabled, name, quantity)
        self.ter = ter

    def __lt__(self, other) -> bool:
        return self.ter > other.ter
