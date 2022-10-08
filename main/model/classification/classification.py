from typing import List

from prompt_toolkit import print_formatted_text, HTML

from main.model.classification.category import Category


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

    def __str__(self) -> str:
        """
        Creates a string with the classifications name, its current value and the strings for all categories.
        :return: the string
        """
        result = self.name
        result += f"\n{self.current_value:.2f}€"
        for category in self.categories:
            result += f"\n  {category}"
        return result

    def calculate_target_values(self, investment_value: float):
        target_value = self.current_value + investment_value
        for category in self.categories:
            category_target_value = target_value * (category.target_allocation / 100)
            category.delta_value = category_target_value - category.current_value
            if category.delta_value > investment_value:
                category.investment_value += investment_value
                investment_value = 0
            elif category.delta_value > 0:
                category.investment_value += category.delta_value
                investment_value -= category.delta_value

    def is_valid(self) -> bool:
        percentage = 0.0
        for category in self.categories:
            percentage += category.target_allocation

        return percentage == 100.0

    def print(self):
        print_formatted_text(
            HTML("<b><u>{:<20} | {:s}</u></b>".format(self.name, "Allocation"))
        )
        for category in self.categories:
            print_formatted_text(
                "{:<20} | {:.2f}%".format(
                    category.name, round(category.current_allocation * 100, 2)
                )
            )
        print_formatted_text("")
