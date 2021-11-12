from main.controller import Configuration
from main.model import Investment


def calculate_current_values():
    print("Calculating current investment values...")
    i = 0
    for investment in Configuration.investments:
        investment.calculate_current_value()
        i += 1
        progress = i / len(Configuration.investments) * 100
        progress_str = "{progress:.2f}%"
        print(progress_str.format(progress=progress))

    for category in Configuration.categories:
        for investment in Configuration.get_investments(category):
            category.current_value += investment.current_value

    for classification in Configuration.classifications:
        classification.calculate_current_value()


def rebalance():
    for category in Configuration.categories:
        investments = Configuration.get_investments(category)
        investments.sort(reverse=True)

        print(category.name + ": " + str(category.investment_value))

        for investment in investments:
            if investment.enabled:
                smallest_delta = get_smallest_delta(investment)
                if category.investment_value < smallest_delta:
                    investment.investment_value += category.investment_value
                    for investment_category in Configuration.investments.get(investment):
                        investment_category.investment_value -= category.investment_value
                else:
                    investment.investment_value += smallest_delta
                    for investment_category in Configuration.investments.get(investment):
                        investment_category.investment_value -= smallest_delta
            else:
                print("Skipping " + investment.name)


def get_smallest_delta(investment: Investment) -> float:
    result = -1.0
    for category in Configuration.investments[investment]:
        if result == -1.0 or category.investment_value < result:
            result = category.investment_value
    return result
