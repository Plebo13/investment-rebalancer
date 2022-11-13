from typing import List, Set
from investment_rebalancer.model.asset.etf import ETF


class Category:
    def __init__(self, name: str, target_allocation: float, etfs: List[ETF]) -> None:
        self.name = name
        self.target_allocation = target_allocation
        self.etfs = etfs
        self.etfs.sort(key=lambda x: x.ter)
        self.current_allocation: float = 0.0
        self.delta_value: float = 0.0
        self.to_invest: float = 0.0

    @property
    def current_value(self) -> float:
        value = 0.0
        for etf in self.etfs:
            value += etf.current_value
        return value

    def invest(self, investment: float, investable_etfs: Set[ETF]) -> float:
        for etf in self.etfs:
            if etf in investable_etfs:
                if self.to_invest < investment:
                    etf.investment += self.to_invest
                    new_investment = investment - self.to_invest
                    self.to_invest = 0.0
                    return new_investment
                else:
                    etf.investment += investment
                    self.to_invest -= investment
                    return 0.0
        return investment

    def __eq__(self, other: object) -> bool:
        """
        Checks whether or not an object is equal to this instance.
        Two categories are equal if they have the same name.
        :param other: the other object
        :return: true if the other object is equal, otherwise false
        """
        if other == self:
            return True
        if not isinstance(other, Category):
            return False
        return other.name == self.name
