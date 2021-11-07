from main.controller import Configuration
from main.model import Investment


def calculate_current_values():
    for category in Configuration.categories:
        for investment in Configuration.get_investments(category):
            category.current_value += investment.current_value

    for classification in Configuration.classifications:
        classification.calculate_current_value()


def rebalance():
    for category in Configuration.categories:
        investments = Configuration.get_investments(category)
        investments.sort(reverse=True)

        for investment in investments:
            if investment.enabled:
                smallest_delta = get_smallest_delta(investment)
                if category.investment_value < smallest_delta:
                    investment.investment_value += category.investment_value
                    category.investment_value = 0.0
                else:
                    investment.investment_value += smallest_delta
                    category.investment_value -= smallest_delta
            else:
                print("Skipping " + investment.name)


def get_smallest_delta(investment: Investment) -> float:
    result = -1.0
    for category in Configuration.investments[investment]:
        if result == -1.0 or category.investment_value < result:
            result = category.investment_value
    return result
