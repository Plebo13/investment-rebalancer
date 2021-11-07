import json
import os
from main.model.Category import Category


from main.model.Classification import Classification
from main.model.Investment import Investment
from main.model.NamedList import NamedList
from main.model.TERInvestment import TERInvestment

CONFIG_PATH = "config.json"

classifications: NamedList[Classification] = []
investments: NamedList[Investment] = []


def config_available() -> bool:
    return os.path.isfile(CONFIG_PATH)


def get_classification(name: str) -> Classification:
    for classification in classifications:
        if classification.name == name:
            return classification
    new_classification = Classification(name)
    classifications.append(new_classification)
    return new_classification


def add_classification(classification: Classification):
    if classification not in classifications:
        classifications.append(classification)


def read():
    with open(CONFIG_PATH) as configuration_file:
        config = json.load(configuration_file)

    # Read all classifications
    classifications_config = config["classifications"]
    for classification_str in classifications_config:
        classification = Classification(classification_str)

        categories_config = classifications_config[classification_str]
        for category_str in categories_config:
            category_config = categories_config[category_str]
            category = Category(category_str, category_config["percentage"])
            classification.categories.append(category)

        classifications.append(classification)

    # Read all investments
    investments_config = config["investments"]
    for investment_str in investments_config:
        name = investments_config[investment_str]["name"]
        quantity = investments_config[investment_str]["quantity"]
        categories = investments_config[investment_str]["categories"]
        if "ter" in investments_config[investment_str]:
            ter = investments_config[investment_str]["ter"]
            investment = TERInvestment(investment_str, name, quantity, ter)

        else:
            investment = Investment(investment_str, name, quantity)

        investment.add_categories(categories)
        investments.append(investment)


def write_classification(classification: Classification, config):
    config[classification.name] = {}

    for category in classification.categories:
        config[classification.name][category.name] = {}
        config[classification.name][category.name]["percentage"] = category.percentage


def write_investment(investment: Investment, config):
    config[investment.isin] = {
        "name": investment.name, "quantity": investment.quantity}
    if isinstance(investment, TERInvestment):
        config[investment.isin]["ter"] = investment.ter

    categories_str = ""
    for category in investment.categories:
        categories_str += category+","
    config[investment.isin]["categories"] = categories_str.strip(",")


def write_configuration():
    config = {}
    config["classifications"] = {}
    for classification in classifications:
        write_classification(classification, config["classifications"])

    config["investments"] = {}
    for investment in investments:
        write_investment(investment, config["investments"])

    with open(CONFIG_PATH, 'w') as configuration_file:
        json.dump(config, configuration_file)
