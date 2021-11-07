from main.model.Investment import Investment
from main.model.Named import Named
from typing import List


class Category(Named):

    def __init__(self, name: str, percentage: float) -> None:
        super().__init__(name)
        self.percentage = percentage
        self.investments: List[Investment] = []

    def __eq__(self, o: object) -> bool:
        if o == self:
            return True
        if not isinstance(o, Category):
            return False
        return o.name == self.name

    def __str__(self) -> str:
        return self.name+": "+str(self.percentage)

    def get_value(self) -> float:
        value = 0.0
        for investment in self.investments:
            value = value + investment.current_value
        return value

    def is_valid(self) -> bool:
        return len(self.investments) > 0
