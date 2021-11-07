import os
import configparser

from main.model.Category import Category
from main.model.Classification import Classification
from main.model.Investment import Investment

CONFIG_PATH = "config.cfg"
categories = list()
classifications = list()
investments = list()
ter_investments = list()


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


def write_configuration():
    config = configparser.ConfigParser()
    for classification in classifications:
        assert isinstance(classification, Classification)
        config[classification.name] = {}
        config[classification.name]['type'] = 'classification'

        categories_str = ""
        for category in classification.categories:
            assert isinstance(category, Category)
            categories_str += category.name + ","
        categories_str = categories_str.strip(',')
        config[classification.name]['categories'] = categories_str

    for category in categories:
        assert isinstance(category, Category)
        config[category.name] = {}
        config[category.name]['type'] = 'category'
        config[category.name]['percentage'] = str(category.percentage)

        investments_str = ""
        for investment in category.investments:
            assert isinstance(investment, Investment)
            investments_str += investment.name + ","
        investments_str = investments_str.strip(',')
        config[category.name]['investments'] = investments_str

    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)
