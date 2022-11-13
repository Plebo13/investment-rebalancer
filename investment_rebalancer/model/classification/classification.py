from typing import List

from investment_rebalancer.model.classification.category import Category
from investment_rebalancer.model.asset.etf import ETF


class Classification:
    def __init__(self, name: str, categories: List[Category]) -> None:
        self.name = name
        self.categories = categories

    @property
    def current_value(self) -> float:
        value = 0.0
        for category in self.categories:
            value += category.current_value
        return value

    def __eq__(self, other: object) -> bool:
        """
        Checks whether or not an object is equal to this instance.
        Two classifications are equal if they have the same name.
        :param other: the other object
        :return: true if the other object is equal, otherwise false
        """
        if other == self:
            return True
        if not isinstance(other, Classification):
            return False
        return super().__eq__(other)

    def calculate_target_values(self, investment_value: float):
        target_value = self.current_value + investment_value
        for category in self.categories:
            category_target_value = target_value * (category.target_allocation / 100)
            category.delta_value = category_target_value - category.current_value
            if category.delta_value > investment_value:
                category.to_invest += investment_value
                investment_value = 0
            elif category.delta_value > 0:
                category.to_invest += category.delta_value
                investment_value -= category.delta_value

    def is_investible(self, etf: ETF) -> bool:
        for category in self.categories:
            if etf in category.etfs and category.to_invest <= 0.0:
                return False
        return True
