from main.controller import Configuration
from main.model.Category import Category

if not Configuration.config_available():
    print("No configuration available.")
    user_input = input("Do you want to add a new category? (Y/n) ").strip()

    while user_input == "" or user_input.lower() == "y":
        name = input("Name: ").strip()
        percentage = float(input("Percentage: ").strip())
        classification = Configuration.get_classification(input("Classification: ").strip())
        category=Category(name, percentage)
        Configuration.categories.append(category)
        classification.categories.append(category)
        user_input = input("Do you want to add another category? (Y/n) ").strip()

    Configuration.write_configuration()
