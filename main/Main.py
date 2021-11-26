import sys

from prompt_toolkit import HTML, print_formatted_text, prompt

from main.controller import Configuration
# Script starts here
from main.controller.NumberValidator import NumberValidator

if len(sys.argv) == 2:
    Configuration.read(sys.argv[1])
else:
    Configuration.read()

total_value = 0.0
for asset in Configuration.assets:
    asset.calculate_current_value()
    total_value += asset.current_value

for asset in Configuration.assets:
    asset.print()

format_str = "<b>Total value: <u>{value:.2f}€</u></b>"
print_formatted_text(HTML(format_str.format(value=total_value)))

investment_value = float(prompt("\nHow much money do you want to invest? ",
                                validator=NumberValidator()))

total_value += investment_value
for asset in Configuration.assets:
    asset.calculate_delta(total_value)
    if asset.delta > investment_value:
        asset.investment_value = investment_value
        investment_value = 0
    elif asset.delta > 0:
        asset.investment_value = asset.delta
        investment_value -= asset.investment_value

    asset.rebalance()

    for investment in asset.investments:
        if investment.investment_value > 0:
            investment.print()
