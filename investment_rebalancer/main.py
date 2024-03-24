import argparse
import os
from pathlib import Path

from prettytable import PrettyTable
from prompt_toolkit import prompt

from investment_rebalancer.controller.number_validator import NumberValidator
from investment_rebalancer.model import configuration


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
        config = configuration.parse(args.config)
    except configuration.ConfigurationException as e:
        print(f"The configuration could not be read: {str(e)}")
        return

    # * Print current status
    print(f"Total investment value: {config.current_value:.2f}€\n")
    config.print_current_allocation()

    # * Calculate target values
    investment_value = float(
        prompt("\nHow much money do you want to invest? ", validator=NumberValidator())
    )
    config.calculate_targets(investment_value)
    config.print_categories_to_invest()

    config.invest(investment_value)

    # # Print all ETF to invest in.
    # print("\nETFs to invest in:")
    # for etf in configuration.etfs.values():
    #     if etf.investment > 0.0:
    #         print(f"{etf.name}: {round(etf.investment)}€")


if __name__ == "__main__":
    main()
