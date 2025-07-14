import argparse
import os
from pathlib import Path

from prompt_toolkit import prompt

from investment_rebalancer.controller.number_validator import NumberValidator
from investment_rebalancer.model import configuration


def main():
    parser = argparse.ArgumentParser(
        prog="Investment Rebalancer",
        description="Calculate investments for rebalancing.",
    )
    parser.add_argument(
        "-c",
        "--config",
        default=os.path.join(Path.home(), ".investment-rebalancer/config.json"),
        help="Config file path",
    )
    parser.add_argument(
        "-i",
        "--invest",
        action="store_true",
        help="Flag whether new money should be invested",
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

    if args.invest:
        # * Calculate target values
        investment_value = float(
            prompt(
                "\nHow much money do you want to invest? ", validator=NumberValidator()
            )
        )
        config.calculate_targets(investment_value)
        config.print_categories_to_invest()

        config.invest(investment_value)

        # * Print all ETF to invest in.
        print("\nETFs to invest in:")
        total_investment = 0.0
        for etf in config.etfs:
            if etf.investment > 0.0:
                print(f"{etf.name}: {round(etf.investment)}€")
                total_investment += etf.investment
        print(f"Total: {total_investment:.2f}€")


if __name__ == "__main__":
    main()
