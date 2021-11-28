import sys

from prettytable import PrettyTable
from prompt_toolkit import HTML, print_formatted_text, prompt

from main.controller import Configuration
from main.controller.NumberValidator import NumberValidator


class Main:
    def __init__(self, configuration_path: str = "config.json"):
        Configuration.read(configuration_path)
        self.total_value = 0.0

    def print_current_asset_allocation(self):
        table = PrettyTable(["Asset", "Allocation", "Value"])
        for asset in Configuration.assets:
            assets_current_allocation = round(asset.current_value / self.total_value * 100, 2)
            table.add_row(
                [asset.name, str(assets_current_allocation) + " %", str(round(asset.current_value, 2)) + " €"])

        table.align = "l"
        print_formatted_text(table.get_string(sortby="Allocation", reversesort=True))
        format_str = "<b>Total value: <u>{value:.2f} €</u></b>"
        print_formatted_text(HTML(format_str.format(value=self.total_value)))

    def start(self):
        # Update current values
        for asset in Configuration.assets:
            asset.calculate_current_value()
            self.total_value += asset.current_value

        self.print_current_asset_allocation()

        investment_value = float(prompt("\nHow much money do you want to invest? ",
                                        validator=NumberValidator()))
        self.rebalance(investment_value)

    def rebalance(self, investment_value):
        self.total_value += investment_value
        for asset in Configuration.assets:
            asset.calculate_delta(self.total_value)
            if asset.delta_value > investment_value:
                asset.investment_value = investment_value
                investment_value = 0
            elif asset.delta_value > 0:
                asset.investment_value = asset.delta_value
                investment_value -= asset.investment_value

            asset.rebalance()


if __name__ == "__main__":
    main: Main
    if len(sys.argv) == 2:
        main = Main(sys.argv[1])
    else:
        main = Main(sys.argv[1])

    main.start()
