import argparse

from prettytable import PrettyTable
from prompt_toolkit import HTML, print_formatted_text, prompt

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
    for classification in configuration.classifications:
        total_value += classification.current_value
    print(f"{total_value:.2f}€")


def __init__(self, configuration_path: str = "config.json"):
    """
    Constructor for a given configuration path.
    :param configuration_path: the configuration path
    """

    self.total_value = 0.0


def print_current_asset_allocation(self):
    table = PrettyTable(["Asset", "Allocation", "Value"])
    # for asset in Configuration.etfs:
    #     assets_current_allocation = round(
    #         asset.current_value / self.total_value * 100, 2
    #     )
    #     table.add_row(
    #         [
    #             asset.name,
    #             str(assets_current_allocation) + " %",
    #             str(round(asset.current_value, 2)) + " €",
    #         ]
    #     )

    table.align = "l"
    print_formatted_text(table.get_string(sortby="Allocation", reversesort=True))
    format_str = "<b>Total value: <u>{value:.2f} €</u></b>"
    print_formatted_text(HTML(format_str.format(value=self.total_value)))


def start(self):
    # Update current values
    # for asset in Configuration.etfs:
    #     asset.calculate_current_value()
    #     self.total_value += asset.current_value

    self.print_current_asset_allocation()

    investment_value = float(
        prompt("\nHow much money do you want to invest? ", validator=NumberValidator())
    )
    self.rebalance(investment_value)

    # for asset in Configuration.etfs:
    #     asset.print_result()


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
