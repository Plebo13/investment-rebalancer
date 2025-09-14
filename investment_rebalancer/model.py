
from typing import List
from pydantic import BaseModel


class ETF(BaseModel):
    name: str
    value: float
    target_allocation: float

    def get_value_difference(self, total_value: float) -> float:
        return self.value-total_value*self.target_allocation

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ETF):
            return False
        return other.name == self.name


class ETFList(List[ETF]):
    def get_value(self) -> float:
        result = 0.0
        for etf in self:
            result += etf.value
        return result

    def rebalance(self):
        min_etf = None
        for etf in self:
            if not min_etf or etf.get_value_difference(self.get_value()) < min_etf.get_value_difference(self.get_value()):
                min_etf = etf

        assert isinstance(min_etf, ETF)

        new_total = min_etf.value/min_etf.target_allocation

        for etf in self:
            new_value = new_total*etf.target_allocation
            print(f"{etf.name}: {new_value-etf.value:.2F}€")
