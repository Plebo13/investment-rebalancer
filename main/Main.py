import sys

from prompt_toolkit import prompt

from main.controller import Configuration, Rebalancer
from main.controller.NumberValidator import NumberValidator

# Script starts here
if len(sys.argv) == 2:
    Configuration.read(sys.argv[1])
else:
    Configuration.read()
Rebalancer.calculate_current_values()

for classification in Configuration.classifications:
    classification.print()

investment_value = float(prompt("How much money do you want to invest? ", validator=NumberValidator()))

for classification in Configuration.classifications:
    classification.calculate_target_values(investment_value)

Rebalancer.rebalance()

for investment in Configuration.investments:
    if investment.investment_value > 0:
        investment.print()
