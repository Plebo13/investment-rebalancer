import os
from typing import List, Set
from prettytable import PrettyTable

import yaml
from pydantic import BaseModel, computed_field
from pydantic_yaml import parse_yaml_raw_as

from investment_rebalancer.model.asset.etf import ETF
from investment_rebalancer.model.classification.category import Category
from investment_rebalancer.model.classification.classification import Classification


class ConfigurationException(BaseException):
    pass


class Configuration(BaseModel):
    classifications: List[Classification]
    etfs: List[ETF]

    @computed_field
    @property
    def current_value(self) -> float:
        value = 0.0
        for etf in self.etfs:
            value += etf.current_value
        return value

    def __get_category_value(
        self, classification: Classification, category_key: str
    ) -> float:
        value = 0.0
        for etf in self.etfs:
            if classification.key not in etf.classifications.keys():
                print(
                    f"ETF {etf.name} not configures for classification {classification.name}"
                )
                continue
            if category_key in etf.classifications[classification.key]:
                value += etf.current_value
        return value

    def __get_category(self, key: str) -> Category:
        for classification in self.classifications:
            if key in classification.categories:
                return classification.categories[key]
        raise ValueError(f"No category with key '{key}'!")

    def __get_investable_etfs(self) -> List[ETF]:
        investable_etfs = []
        for etf in self.etfs:
            investible = True

            for category in etf.classifications.values():
                if self.__get_category(category).to_invest <= 0.0:
                    investible = False
                    break

            if investible:
                investable_etfs.append(etf)
        investable_etfs.sort(key=lambda x: x.ter)
        return investable_etfs

    def __get_all_categories(self) -> List[Category]:
        categories = []
        for classification in self.classifications:
            for category in classification.categories.values():
                if category.to_invest > 0.0:
                    categories.append(category)
        categories.sort(key=lambda x: x.to_invest)
        return categories

    def print_current_allocation(self):
        for classification in self.classifications:
            print(f"{classification.name}:")
            table = PrettyTable(["Category", "Value", "Allocation", "Target"])
            for key, category in classification.categories.items():
                category_value = self.__get_category_value(classification, key)
                current_allocation = category_value / self.current_value * 100
                table.add_row(
                    [
                        category.name,
                        f"{category_value:.2f}€",
                        f"{current_allocation:.2f}%",
                        f"{category.target_allocation:.2f}%",
                    ]
                )

            table.align = "l"
            print(table.get_string(sortby="Allocation", reversesort=True))

    def calculate_targets(self, investment_value: float):
        for classification in self.classifications:
            target_value = self.current_value + investment_value
            for key, category in classification.categories.items():
                category_target_value = target_value * (
                    category.target_allocation / 100
                )
                category.delta_value = (
                    category_target_value
                    - self.__get_category_value(classification, key)
                )
                if category.delta_value > investment_value:
                    category.to_invest += investment_value
                    investment_value = 0
                elif category.delta_value > 0:
                    category.to_invest += category.delta_value
                    investment_value -= category.delta_value

    def print_categories_to_invest(self):
        print("\nCategories to invest in:")
        for classification in self.classifications:
            for category in classification.categories.values():
                if category.to_invest > 0.0:
                    print(f"{category.name}: {category.to_invest:.2f}€")

    def invest(self, investment_value: float):
        investable_categories = self.__get_all_categories()
        while len(investable_categories) > 0 and round(investment_value, 2) > 0.0:
            investment_value = investable_categories[0].invest(
                investment_value, self.__get_investable_etfs()
            )
            investable_categories = self.__get_all_categories()


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
