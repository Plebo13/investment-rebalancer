import json
import os

from main.model.NamedList import NamedList
from main.model.Category import Category
from main.model.Classification import Classification
from main.model.Investment import Investment
from main.model.TERInvestment import TERInvestment

CONFIG_PATH = "config.json"
classifications: NamedList[Classification] = []
categories: NamedList[Category] = []
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


def add_category(category: Category):
    if category not in categories:
        categories.append(category)


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

    with open(CONFIG_PATH, 'w') as configfile:
        json.dump(config, configfile)
