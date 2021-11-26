import json
import os

from main.model.Asset import Asset
from main.model.Category import Category
from main.model.Classification import Classification
from main.model.Investment import Investment
from main.model.NamedList import NamedList
from main.model.TERInvestment import TERInvestment

DEFAULT_CONFIG_PATH = "config.json"

assets: NamedList[Asset] = NamedList()


def config_available(config_path=DEFAULT_CONFIG_PATH) -> bool:
    return os.path.isfile(config_path)


def read(config_path=DEFAULT_CONFIG_PATH):
    with open(config_path) as configuration_file:
        config = json.load(configuration_file)

    # Read assets
    assets_config = config["assets"]
    for asset_name in assets_config:
        asset = Asset(asset_name,
                      float(assets_config[asset_name]["percentage"]))
        parse_classifications(asset, assets_config[asset_name])
        asset.validate()
        assets.append(asset)


def parse_classifications(asset, asset_config):
    classifications_config = asset_config["classifications"]
    for classification_config in classifications_config:
        classification = Classification(classification_config)

        categories_config = classifications_config[classification_config]
        for category_str in categories_config:
            category_config = categories_config[category_str]
            category = Category(category_str, category_config["percentage"])
            classification.categories.append(category)

        asset.classifications.append(classification)

    parse_investments(asset, asset_config)


def parse_investments(asset, asset_config):
    investments_config = asset_config["investments"]
    for investment_str in investments_config:
        name = investments_config[investment_str]["name"]
        enabled = investments_config[investment_str]["enabled"]
        quantity = investments_config[investment_str]["quantity"]
        categories_str = investments_config[investment_str][
            "categories"].split(
            ",")
        if "ter" in investments_config[investment_str]:
            ter = investments_config[investment_str]["ter"]
            investment = TERInvestment(investment_str, enabled, name,
                                       quantity,
                                       ter)

        else:
            investment = Investment(investment_str, enabled, name, quantity)

        categories_named_list: NamedList[Category] = NamedList()
        for category_str in categories_str:
            categories_named_list.append(
                asset.get_all_categories().get(category_str))

        asset.investments[investment] = categories_named_list
