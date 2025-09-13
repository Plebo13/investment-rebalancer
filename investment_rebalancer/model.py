
from typing import List
from pydantic import BaseModel


class ETF(BaseModel):
    name: str
    value: float
    current_allocation: float = 0.0
    target_allocation: float

    def get_allocation_diff(self) -> float:
        return self.current_allocation-self.target_allocation

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

    def calculate_current_allocations(self):
        total_value = self.get_value()

        for etf in self:
            etf.current_allocation = round(etf.value/total_value, 4)

    def rebalance(self):
        min_etf = None
        for etf in self:
            if not min_etf or etf.get_allocation_diff() < min_etf.get_allocation_diff():
                min_etf = etf

        assert isinstance(min_etf, ETF)

        new_total = min_etf.value/min_etf.target_allocation

        for etf in self:
            new_value = new_total*etf.target_allocation
            print(f"{etf.name}: {new_value-etf.value:.2F}€")
