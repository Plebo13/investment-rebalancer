import json
import os
from typing import Dict, List, Set

from sharepp import SharePP
from investment_rebalancer.model.errors import ConfigurationException
from investment_rebalancer.model.asset.etf import ETF
from investment_rebalancer.model.classification.category import Category
from investment_rebalancer.model.classification.classification import Classification

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
            name = etf_config[etf]["name"]
            print(f"Getting current price for {name}")
            current_price = SharePP.get_etf_price(etf)
            # current_price = 5.0
            etfs[etf] = ETF(
                etf,
                name,
                etf_config[etf]["enabled"],
                etf_config[etf]["quantity"],
                current_price,
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


def get_investable_etfs() -> Set[ETF]:
    investable_etfs: Set[ETF] = []
    for isin in etfs:
        investible = True
        for classification in classifications:
            if not classification.is_investible(etfs[isin]):
                investible = False
                break
        if investible:
            investable_etfs.append(etfs[isin])
    return investable_etfs


def get_all_categories() -> List[Category]:
    categories: List[Category] = []
    for classification in classifications:
        for category in classification.categories:
            if category.to_invest > 0.0:
                categories.append(category)
    categories.sort(key=lambda x: x.to_invest)
    return categories
