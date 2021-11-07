from main.controller import Configuration
from main.model.Category import Category
from main.model.TERInvestment import TERInvestment


def create_new_configuration():
    print("No configuration available.")
    user_input = input("Do you want to add a new category? (Y/n) ").strip()

    while user_input == "" or user_input.lower() == "y":
        name = input("Name: ").strip()
        percentage = float(input("Percentage: ").strip())
        classification = Configuration.get_classification(
            input("Classification: ").strip())

        category = Category(name, percentage)
        Configuration.categories.append(category)
        classification.categories.append(category)
        user_input = input(
            "Do you want to add another category? (Y/n) ").strip()

    user_input = input(
        "Do you want to add an investment? (Y/n) ").strip()
    while user_input == "" or user_input.lower() == "y":
        name = input("Name: ").strip()
        isin = input("ISIN: ").strip()
        quantity = float(input("Quantity: ").strip())
        ter = float(input("TER: ").strip())
        categories = input("Categories: ").strip()

        investment = TERInvestment(isin, name, quantity, ter)
        investment.add_categories(categories)
        Configuration.investments.append(investment)
        user_input = input(
            "Do you want to add another investment? (Y/n) ").strip()

    Configuration.write_configuration()


if not Configuration.config_available():
    create_new_configuration()
