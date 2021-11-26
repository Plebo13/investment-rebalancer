import sys

from prompt_toolkit import HTML, print_formatted_text

from main.controller import Configuration

# Script starts here
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

# investment_value = float(prompt("\nHow much money do you want to invest? ", validator=NumberValidator()))
#
# for classification in Configuration.classifications:
#     classification.calculate_target_values(investment_value)
#
# Rebalancer.rebalance()
#
# for investment in Configuration.investments:
#     if investment.investment_value > 0:
#         investment.print()
