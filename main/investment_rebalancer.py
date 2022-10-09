import argparse

from prettytable import PrettyTable
from prompt_toolkit import prompt

from main.model import configuration
from main.model.errors import ConfigurationException
from main.controller.NumberValidator import NumberValidator


def main(config_path: str):
    try:
        configuration.parse(config_path)
    except ConfigurationException as e:
        print(f"The configuration could not be read: {str(e)}")
        return

    total_value = 0.0
    for etf in configuration.etfs:
        total_value += configuration.etfs[etf].current_value

    print(f"Total investment value: {total_value:.2f}€\n")

    for classification in configuration.classifications:
        print(f"{classification.name}:")
        table = PrettyTable(["Category", "Value", "Allocation", "Target"])
        for category in classification.categories:
            current_allocation = category.current_value / total_value * 100
            table.add_row(
                [
                    category.name,
                    f"{category.current_value:.2f}€",
                    f"{current_allocation:.2f}%",
                    f"{category.target_allocation:.2f}%",
                ]
            )

        table.align = "l"
        print(table.get_string(sortby="Allocation", reversesort=True))

    investment_value = float(
        prompt("\nHow much money do you want to invest? ", validator=NumberValidator())
    )

    for classification in configuration.classifications:
        classification.calculate_target_values(investment_value)

    for classification in configuration.classifications:
        for category in classification.categories:
            print(f"{category.name}: {category.to_invest:.2f}€")

    print("\n")
    for etf in configuration.get_investable_etfs():
        print(etf.name)

    print("\n")
    for category in configuration.get_all_categories():
        print(f"{category.name}: {category.to_invest:.2f}€")

    print("\n")
    investable_categories = configuration.get_all_categories()
    while len(investable_categories) > 0 and investment_value > 0.0:
        print(f"Investing {investment_value:.2f}€ in {investable_categories[0].name}")
        investment_value = investable_categories[0].invest(
            investment_value, configuration.get_investable_etfs()
        )
        print(f"New investment value: {investment_value:.2f}€")
        investable_categories = configuration.get_all_categories()
        print(f"New length of categories: {len(investable_categories)}")

    print("\n")
    for etf in configuration.etfs.values():
        print(f"{etf.name}: {etf.investment:.2f}€")


def rebalance(self, investment_value):
    self.total_value += investment_value
    # for asset in Configuration.etfs:
    #     asset.calculate_delta(self.total_value)
    #     if asset.delta_value > investment_value:
    #         asset.investment_value = investment_value
    #         investment_value = 0
    #     elif asset.delta_value > 0:
    #         asset.investment_value = asset.delta_value
    #         investment_value -= asset.investment_value

    #     asset.rebalance()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate investments for rebalancing."
    )
    parser.add_argument("-c", "--config", default="config.json")
    args = parser.parse_args()
    main(args.config)
