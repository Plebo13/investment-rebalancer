import json
import os
from typing import Dict, List, Set

from sharepp import SharePP
from main.model.errors import ConfigurationException
from main.model.asset.etf import ETF
from main.model.asset.DeepAsset import DeepAsset
from main.model.classification.category import Category
from main.model.classification.classification import Classification

etfs: Dict[str, ETF] = {}
classifications: List[Classification] = []


def parse(config_path: str):
    if not os.path.isfile(config_path):
        raise ConfigurationException(
            f"The given configuration file does not exist: {config_path}"
        )

    with open(config_path) as configuration_file:
        config = json.load(configuration_file)

    # Read etf configs
    etf_config = config["etf"]
    for etf in etf_config:
        try:
            etfs[etf] = ETF(
                etf_config[etf]["name"],
                etf_config[etf]["enabled"],
                etf_config[etf]["quantity"],
                SharePP.get_etf_price(etf),
                etf_config[etf]["ter"],
            )
        except KeyError as e:
            raise ConfigurationException(f"Key {str(e)} missing in ETF {etf}!")

    if not etfs:
        raise ConfigurationException("No ETFs configured!")

    # Read classification configs
    classification_config = config["classifications"]
    for classification in classification_config:
        try:
            classifications.append(
                parse_classification(
                    classification, classification_config[classification]
                )
            )
        except KeyError as e:
            raise ConfigurationException(
                f"Key {str(e)} missing in classification {classification}!"
            )

    if not classifications:
        raise ConfigurationException("No classifications configured!")


def parse_classification(name: str, categories_config) -> Classification:
    categories: Set[Category] = []
    for category_config in categories_config:
        assets: List[ETF] = []
        for asset_config in categories_config[category_config]["assets"]:
            assets.append(etfs[asset_config])
        categories.append(
            Category(
                category_config,
                categories_config[category_config]["target_allocation"],
                assets,
            )
        )
    return Classification(name, categories)


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
