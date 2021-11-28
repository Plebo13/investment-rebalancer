from typing import List

from prompt_toolkit import print_formatted_text, HTML

from main.model.Named import Named
from main.model.classification.Category import Category


class Classification(Named):
    def __init__(self, name: str):
        """
        Constructor for a given name.
        :param name: the name of the classification
        """
        super().__init__(name)
        self.current_value = 0.0
        self.categories: List[Category] = []

    def __eq__(self, o: object) -> bool:
        """
        Checks whether or not an object is equal to this instance.
        Two classifications are equal if they have the same name.
        :param o: the other object
        :return: true if the other object is equal, otherwise false
        """
        if o == self:
            return True
        if not isinstance(o, Classification):
            return False
        return super().__eq__(o)

    def __str__(self) -> str:
        """
        Creates a string with the classifications name, its current value and the strings for all categories.
        :return: the string
        """
        result = self.name
        result += "\n" + str(self.current_value)
        for category in self.categories:
            result += "\n    " + str(category)
        return result

    def calculate_current_value(self):
        for category in self.categories:
            self.current_value += category.current_value

        for category in self.categories:
            category.allocation = round(
                category.current_value / self.current_value, 4)

    def calculate_target_values(self, investment_value: float):
        target_value = self.current_value + investment_value
        for category in self.categories:
            category_target_value = target_value * (category.percentage / 100)
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
            percentage += category.percentage

        return percentage == 100.0

    def print(self):
        print_formatted_text(
            HTML("<b><u>{:<20} | {:s}</u></b>".format(self.name, "Allocation")))
        for category in self.categories:
            print_formatted_text("{:<20} | {:.2f}%".format(category.name, round(
                category.allocation * 100, 2)))
        print_formatted_text("")
