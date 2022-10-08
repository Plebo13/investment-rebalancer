from typing import List
from main.model.asset.etf import ETF


class Category:
    def __init__(self, name: str, target_allocation: float, etfs: List[ETF]) -> None:
        self.name = name
        self.target_allocation = target_allocation
        self.etfs = etfs
        self.current_allocation: float = 0.0
        self.delta_value: float = 0.0
        self.investment: float = 0.0

    @property
    def current_value(self) -> float:
        value = 0.0
        for etf in self.etfs:
            value += etf.current_value
        return value

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

    def __str__(self) -> str:
        """
        Creates a string with the classifications name and its investment value.
        :return: the string
        """
        return f"{self.name}: {self.investment:.2f}€"
