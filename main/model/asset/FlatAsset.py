from typing import List

from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import ProgressBar

from main.model.asset.AbstractAsset import AbstractAsset
from main.model.investment.BaseInvestment import BaseInvestment


class FlatAsset(AbstractAsset):
    def __init__(self, name: str, percentage: float):
        """
        Constructor for a given name and a given allocation.
        :param name: the name of the asset
        :param percentage: the allocation for that asset
        """
        super().__init__(name, percentage)
        self.target_value = 0.0
        self.investments: List[BaseInvestment] = []

    def print(self):
        print_formatted_text("")
        format_str = "<b>{name}: {value:.2f}€</b>"
        print_formatted_text(HTML(format_str.format(name=self.name, value=self.current_value)))

        print_formatted_text(HTML("<b><u>{:<15} | {:s}</u></b>".format("Coin", "Value")))
        for investment in self.investments:
            current_allocation = round(investment.current_value / self.current_value * 100, 2)
            print_formatted_text("{:<15} | {:.2f}%".format(investment.name, current_allocation))
        print_formatted_text("")

    def validate(self):
        total_allocation = 0.0
        for investment in self.investments:
            total_allocation += investment.allocation
        return total_allocation == 100.0

    def calculate_current_value(self):
        with ProgressBar(title="Updating " + self.name.lower()) as progress_bar:
            for investment in progress_bar(self.investments, total=len(self.investments)):
                investment.calculate_current_value()
                self.current_value += investment.current_value

    def calculate_delta(self, total_value: float):
        self.target_value = total_value * self.percentage / 100
        self.delta_value = self.target_value - self.current_value

    def rebalance(self):
        for investment in self.investments:
            investment_target_value = self.target_value * investment.allocation / 100
            investment_delta_value = investment_target_value - investment.current_value
            if self.investment_value < investment_delta_value:
                investment.investment_value += self.investment_value
                self.investment_value = 0
            elif investment_delta_value > 0:
                investment.investment_value = investment_delta_value
                self.investment_value -= investment_delta_value
