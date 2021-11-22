from prompt_toolkit import prompt

from main.controller import Configuration, Rebalancer
from main.controller.NumberValidator import NumberValidator

# Script starts here
Configuration.read()
Rebalancer.calculate_current_values()

investment_value = float(prompt("How much money do you want to invest? ", validator=NumberValidator()))

for classification in Configuration.classifications:
    classification.calculate_target_values(investment_value)

Rebalancer.rebalance()

for investment in Configuration.investments:
    if investment.investment_value > 0:
        investment.print()
