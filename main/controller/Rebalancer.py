from main.controller import Configuration


def calculate_current_values():
    for category in Configuration.categories:
        for investment in Configuration.get_investments(category):
            category.current_value += investment.current_value

    for classification in Configuration.classifications:
        classification.calculate_current_value()
