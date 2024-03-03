import os
from typing import List, Set

import yaml
from pydantic import BaseModel
from pydantic_yaml import parse_yaml_raw_as

from investment_rebalancer.model.asset.etf import ETF
from investment_rebalancer.model.classification.category import Category
from investment_rebalancer.model.classification.classification import Classification


class ConfigurationException(BaseException):
    pass


class Configuration(BaseModel):
    classifications: List[Classification]
    etfs: List[ETF]

    def get_investable_etfs(self) -> Set[ETF]:
        """Returns all investible ETF's.
        An investible ETF is one that is not part of a classification in which should not be invested.

        :return: set of all investible ETF's
        """
        investable_etfs: Set[ETF] = []
        for etf in self.etfs:
            investible = True
            for classification in self.classifications:
                if not classification.is_investible(etf):
                    investible = False
                    break
            if investible:
                investable_etfs.append(etf)
        return investable_etfs

    def get_all_categories(self) -> List[Category]:
        categories: List[Category] = []
        for classification in self.classifications:
            for category in classification.categories:
                if category.to_invest > 0.0:
                    categories.append(category)
        categories.sort(key=lambda x: x.to_invest)
        return categories


def parse(config_path: str) -> Configuration:
    # * Check if configuration file exists
    if not os.path.isfile(config_path):
        raise ConfigurationException(
            f"The given configuration file does not exist: {config_path}"
        )

    # * Load configuration data
    with open(config_path) as config_file:
        config_data = config_file.read()

    return parse_yaml_raw_as(Configuration, config_data)
