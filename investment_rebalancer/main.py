import argparse
import os
from pathlib import Path

from prettytable import PrettyTable
from prompt_toolkit import prompt

from investment_rebalancer.controller.number_validator import NumberValidator
from investment_rebalancer.model import configuration
from investment_rebalancer.model.errors import ConfigurationException


def main():
    parser = argparse.ArgumentParser(
        description="Calculate investments for rebalancing."
    )
    parser.add_argument(
        "-c",
        "--config",
        default=os.path.join(Path.home(), ".investment-rebalancer/config.json"),
    )
    args = parser.parse_args()

    try:
        configuration.parse(args.config)
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

    # Print all categories with a delta.
    print("\nCategories to invest in:")
    for classification in configuration.classifications:
        for category in classification.categories:
            if category.to_invest > 0.0:
                print(f"{category.name}: {category.to_invest:.2f}€")

    investable_categories = configuration.get_all_categories()
    while len(investable_categories) > 0 and round(investment_value, 2) > 0.0:
        investment_value = investable_categories[0].invest(
            investment_value, configuration.get_investable_etfs()
        )
        investable_categories = configuration.get_all_categories()

    # Print all ETF to invest in.
    print("\nETFs to invest in:")
    for etf in configuration.etfs.values():
        if etf.investment > 0.0:
            print(f"{etf.name}: {round(etf.investment)}€")


if __name__ == "__main__":
    main()
