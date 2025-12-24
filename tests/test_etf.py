import random
import unittest

from investment_rebalancer.model.asset.etf import ETF


class ETFTest(unittest.TestCase):
    def test_invalid_isin(self):
        with self.assertRaises(ValueError) as cm:
            ETF(isin="1234", name="test etf", current_price=1.0, ter=0.1)
        self.assertTrue("1234 is not a valid ISIN!" in str(cm.exception))

    def test_value_calculation(self):
        current_price = random.uniform(0.1, 9.9)
        quantity = random.randint(1, 99)
        etf = ETF(
            isin="LU1781541179",
            name="test etf",
            current_price=current_price,
            quantity=quantity,
            ter=0.1,
        )
        self.assertEqual(current_price * quantity, etf.current_value)

    def test_equals(self):
        current_price = random.uniform(0.1, 9.9)
        quantity = random.randint(1, 99)
        etf1 = ETF(
            isin="LU1781541179",
            name="test etf",
            current_price=current_price,
            quantity=quantity,
            ter=0.1,
        )
        etf2 = ETF(
            isin="LU1781541179",
            name="test etf",
            current_price=current_price,
            quantity=quantity,
            ter=0.1,
        )
        self.assertEqual(etf1, etf2)

        etf1 = ETF(
            isin="LU1781541179",
            name="test etf",
            current_price=current_price,
            quantity=quantity,
            ter=0.1,
        )
        etf2 = ETF(
            isin="LU0635178014",
            name="test etf",
            current_price=current_price,
            quantity=quantity,
            ter=0.1,
        )
        self.assertNotEqual(etf1, etf2)
