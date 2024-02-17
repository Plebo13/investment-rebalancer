import os
from typing import Dict, List, Optional, Set
from bs4 import BeautifulSoup
from pydantic_core import ValidationError
from pydantic_xml import BaseXmlModel, element

from investment_rebalancer.model.errors import (
    ConfigurationException,
)
from investment_rebalancer.model.asset.etf import ETF
from investment_rebalancer.model.classification.category import Category
from investment_rebalancer.model.classification.classification import Classification

etfs: Dict[str, ETF] = {}
classifications: List[Classification] = []


class Security(BaseXmlModel, tag="security"):
    uuid: str = element(tag="uuid")
    name: str = element(tag="name")
    isin: Optional[str] = element(tag="isin", default=None)


def parse(config_path: str):
    if not os.path.isfile(config_path):
        raise ConfigurationException(
            f"The given configuration file does not exist: {config_path}"
        )

    with open(config_path) as config_file:
        config = config_file.read()

    xml = BeautifulSoup(config, "xml")
    securities: List[Security] = list()
    errors = []
    for security in xml.find("securities"):
        security = str(security).strip()
        if security:
            try:
                securities.append(Security.from_xml(security))
            except ValidationError:
                errors.append(security)

    print(f"Warning: Could not parse {len(errors)} securities.")
    print(f"Parsed {len(securities)} securities.")


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
