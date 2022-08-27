import json
import os

from sharepp import Coin
from main.model.Errors import ConfigurationException
from main.model.NamedList import NamedList
from main.model.asset.AbstractAsset import AbstractAsset
from main.model.asset.DeepAsset import DeepAsset
from main.model.asset.FlatAsset import FlatAsset
from main.model.classification.Category import Category
from main.model.classification.Classification import Classification
from main.model.investment.BaseInvestment import BaseInvestment
from main.model.investment.CryptoInvestment import CryptoInvestment
from main.model.investment.ETFInvestment import ETFInvestment
from main.model.investment.TERInvestment import TERInvestment

DEFAULT_CONFIG_PATH = "config.json"

assets: NamedList[AbstractAsset] = NamedList()


class Configuration:
    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH) -> None:
        if not os.path.isfile(config_path):
            raise ConfigurationException(
                f"The given configuration does not exist: {config_path}"
            )
        self.config_path = config_path
        self.assets: NamedList[AbstractAsset] = NamedList()

    def parse(self):
        with open(self.config_path) as configuration_file:
            config = json.load(configuration_file)

        # Read assets
        assets_config = config["assets"]
        for asset_name in assets_config:
            asset: AbstractAsset
            allocation = float(assets_config[asset_name]["allocation"])
            if "classifications" in assets_config[asset_name]:
                asset = DeepAsset(asset_name, allocation)
                assert isinstance(asset, DeepAsset)
                # parse_classifications(asset, assets_config[asset_name])
            else:
                asset = FlatAsset(asset_name, allocation)
                assert isinstance(asset, FlatAsset)
                # parse_allocated_investments(asset, assets_config[asset_name])

            asset.validate()
            assets.append(asset)

    def parse_classifications(asset: DeepAsset, asset_config):
        classifications_config = asset_config["classifications"]
        for classification_config in classifications_config:
            classification = Classification(classification_config)
            categories_config = classifications_config[classification_config]
            for category_str in categories_config:
                category_config = categories_config[category_str]
                category = Category(category_str, category_config["allocation"])
                classification.categories.append(category)

            asset.classifications.append(classification)

        # parse_investments(asset, asset_config)

    def parse_investments(asset, asset_config):
        investments_config = asset_config["investments"]
        for investment_id in investments_config:
            investment: BaseInvestment
            name = investments_config[investment_id]["name"]
            enabled = investments_config[investment_id]["enabled"]
            quantity = investments_config[investment_id]["quantity"]
            if investments_config[investment_id]["type"] == "etf":
                categories_str = investments_config[investment_id]["categories"].split(
                    ","
                )
                if "ter" in investments_config[investment_id]:
                    ter = investments_config[investment_id]["ter"]
                    investment = TERInvestment(
                        investment_id, enabled, name, quantity, ter
                    )
                else:
                    investment = ETFInvestment(investment_id, enabled, name, quantity)

                categories_list: NamedList[Category] = NamedList()
                for category_str in categories_str:
                    categories_list.append(asset.get_all_categories().get(category_str))

                asset.investments[investment] = categories_list
            else:
                format_string = "Unknown investment type '{type}'!"
                raise ConfigurationException(
                    format_string.format(type=investments_config[investment_id]["type"])
                )

    def parse_allocated_investments(asset: FlatAsset, asset_config):
        investments_config = asset_config["investments"]
        for investment_id in investments_config:
            investment: BaseInvestment
            name = investments_config[investment_id]["name"]
            enabled = investments_config[investment_id]["enabled"]
            quantity = investments_config[investment_id]["quantity"]
            allocation = float(investments_config[investment_id]["allocation"])
            if investments_config[investment_id]["type"] == "etf":
                investment = ETFInvestment(
                    investment_id, enabled, name, quantity, allocation
                )
            elif investments_config[investment_id]["type"] == "crypto":
                coin = Coin(investment_id)
                investment = CryptoInvestment(coin, enabled, name, quantity, allocation)
            else:
                format_string = "Unknown investment type '{type}'!"
                raise ConfigurationException(
                    format_string.format(type=investments_config[investment_id]["type"])
                )

            asset.investments.append(investment)
