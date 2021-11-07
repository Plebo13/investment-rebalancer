from functools import total_ordering

from main.model.Investment import Investment


@total_ordering
class TERInvestment(Investment):

    def __init__(self, isin: str, enabled: bool, name: str, quantity: float, ter: float) -> None:
        super().__init__(isin, enabled, name, quantity)
        self.ter = ter

    def __lt__(self, other) -> bool:
        return self.ter > other.ter
