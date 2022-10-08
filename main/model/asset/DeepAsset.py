from typing import List, Dict

from prettytable import PrettyTable
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import ProgressBar

from main.model.named_list import NamedList
from main.model.asset.AbstractAsset import AbstractAsset
from main.model.classification.category import Category
from main.model.classification.classification import Classification
from main.model.investment.ETFInvestment import ETFInvestment
from main.model.errors import ConfigurationException


class DeepAsset(AbstractAsset):
    def __init__(self, name: str, target_allocation: float):
        super().__init__(name, target_allocation)
        self.classifications: List[Classification] = []
        self.investments: Dict[ETFInvestment, NamedList[Category]] = dict()

    def print(self):
        print_formatted_text("")
        format_str = "<b>{name}: {value:.2f}€</b>"
        print_formatted_text(
            HTML(format_str.format(name=self.name, value=self.current_value))
        )

        for classification in self.classifications:
            classification.print()

    def validate(self):
        for classification in self.classifications:
            if not classification.is_valid():
                error_message = "The sum of all percentages in classification '{classification:s}' is not 100!"
                raise ConfigurationException(
                    error_message.format(classification=classification.name)
                )

    def calculate_current_value(self):
        with ProgressBar(title="Updating " + self.name.lower()) as progress_bar:
            investments = self.investments.keys()
            for investment in progress_bar(investments, total=len(investments)):
                investment.calculate_current_value()
                self.current_value += investment.current_value

        for classification in self.classifications:
            for category in classification.categories:
                for investment in self.get_investments(category):
                    category.current_value += investment.current_value
            classification.calculate_current_value()

    def get_all_categories(self) -> NamedList:
        result: NamedList[Category] = NamedList()
        for classification in self.classifications:
            result.extend(classification.categories)
        return result

    def get_investments(self, category: Category) -> List:
        result: List[ETFInvestment] = []
        for investment in self.investments:
            if self.investments[investment].contains(category.name):
                result.append(investment)
        return result

    def rebalance(self):
        self.calculate_target_values()
        for category in self.get_all_categories():
            investments = self.get_investments(category)
            investments.sort(reverse=True)

            for investment in investments:
                if investment.enabled:
                    smallest_delta = self.get_smallest_delta(investment)
                    if category.investment_value < smallest_delta:
                        investment.investment_value += category.investment_value
                        for investment_category in self.investments.get(investment):
                            investment_category.investment_value -= (
                                category.investment_value
                            )
                    else:
                        investment.investment_value += smallest_delta
                        for investment_category in self.investments.get(investment):
                            investment_category.investment_value -= smallest_delta

    def get_smallest_delta(self, investment: ETFInvestment) -> float:
        result = -1.0
        for category in self.investments[investment]:
            if result == -1.0 or category.investment_value < result:
                result = category.investment_value
        return result

    def calculate_target_values(self):
        for classification in self.classifications:
            classification.calculate_target_values(self.investment_value)

    def print_result(self):
        table = PrettyTable(["Investment", "Invest"])
        for investment in self.investments.keys():
            if investment.investment_value > 0:
                table.add_row(
                    [investment.name, str(round(investment.investment_value, 2)) + " €"]
                )

        if len(table.rows) > 0:
            table.align = "l"
            print_formatted_text(table.get_string(sortby="Invest", reversesort=True))
