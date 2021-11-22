import json
import os
from typing import Dict, List

from main.model.Category import Category
from main.model.Classification import Classification
from main.model.Investment import Investment
from main.model.NamedList import NamedList
from main.model.TERInvestment import TERInvestment
from main.model.exception.ConfigurationException import ConfigurationException

CONFIG_PATH = "config.json"

classifications: NamedList[Classification] = NamedList()
categories: NamedList[Category] = NamedList()
investments: Dict[Investment, NamedList[Category]] = dict()


def config_available() -> bool:
    return os.path.isfile(CONFIG_PATH)


def get_investments(category: Category) -> List:
    result: List[Investment] = []
    for investment in investments:
        if investments[investment].contains(category.name):
            result.append(investment)
    return result


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
            categories.append(category)

        classifications.append(classification)

    # Read all investments
    investments_config = config["investments"]
    for investment_str in investments_config:
        name = investments_config[investment_str]["name"]
        enabled = investments_config[investment_str]["enabled"]
        quantity = investments_config[investment_str]["quantity"]
        categories_str = investments_config[investment_str]["categories"].split(
            ",")
        if "ter" in investments_config[investment_str]:
            ter = investments_config[investment_str]["ter"]
            investment = TERInvestment(investment_str, enabled, name, quantity, ter)

        else:
            investment = Investment(investment_str, enabled, name, quantity)

        categories_named_list: NamedList[Category] = NamedList()
        for category_str in categories_str:
            categories_named_list.append(categories.get(category_str))

        investments[investment] = categories_named_list

        for classification in classifications:
            if not classification.is_valid():
                error_message = "The sum of all percentages in classification '{classification:s}' is not 100!"
                raise ConfigurationException(error_message.format(classification=classification.name))
