from main.model.Category import Category
from main.model.Named import Named
from typing import List


class Classification(Named):
    def __init__(self, name: str):
        super().__init__(name)
        self.current_value = 0.0
        self.categories: List[Category] = []

    def __eq__(self, o: object) -> bool:
        if o == self:
            return True
        if not isinstance(o, Classification):
            return False
        return o.name == self.name

    def __str__(self) -> str:
        result = self.name
        result += "\n" + str(self.current_value)
        for category in self.categories:
            result += "\n    " + str(category)
        return result

    def calculate_current_value(self):
        for category in self.categories:
            self.current_value += category.current_value

    def calculate_target_values(self, investment_value: float):
        target_value = self.current_value + investment_value
        for category in self.categories:
            category_target_value = target_value * (category.percentage / 100)
            category.delta_value = category_target_value - category.current_value
            if category.delta_value > 0:
                if category.delta_value > investment_value:
                    category.investment_value += investment_value
                    investment_value = 0
                else:
                    category.investment_value += category.delta_value
                    investment_value -= category.delta_value
