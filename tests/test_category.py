import random
import unittest

from investment_rebalancer.model.asset.etf import ETF
from investment_rebalancer.model.classification.category import Category


class CategoryTest(unittest.TestCase):
    def test_value_calculation(self):
        current_price1 = random.uniform(0.1, 9.9)
        quantity1 = random.randint(1, 99)
        etf1 = ETF(
            isin="LU1781541179",
            name="test etf",
            current_price=current_price1,
            quantity=quantity1,
            ter=0.2,
        )
        current_price2 = random.uniform(0.1, 9.9)
        quantity2 = random.randint(1, 99)
        etf2 = ETF(
            isin="LU1781541179",
            name="test etf",
            current_price=current_price2,
            quantity=quantity2,
            ter=0.1,
        )
        category = Category("test category", 25.0, [etf1, etf2])
        self.assertEqual(
            category.current_value,
            current_price1 * quantity1 + current_price2 * quantity2,
        )

    def test_equals(self):
        category1 = Category("test category1", 25.0, [])
        category2 = Category("test category1", 25.0, [])
        category3 = Category("test category2", 25.0, [])
        self.assertEqual(category1, category2)
        self.assertNotEqual(category1, category3)
        self.assertNotEqual(category1, None)

    def test_invest(self):
        current_price1 = random.uniform(0.1, 9.9)
        quantity1 = random.randint(1, 99)
        etf1 = ETF(
            isin="LU1781541179",
            name="test etf",
            current_price=current_price1,
            quantity=quantity1,
            ter=0.2,
        )
        current_price2 = random.uniform(0.1, 9.9)
        quantity2 = random.randint(1, 99)
        etf2 = ETF(
            isin="LU1781541179",
            name="test etf",
            current_price=current_price2,
            quantity=quantity2,
            ter=0.1,
        )
        category = Category("test category1", 25.0, [etf1, etf2])
        invest = category.invest(123.0, [etf1])
        self.assertEqual(invest, 123.0)
