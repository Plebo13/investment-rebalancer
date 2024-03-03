import random
import unittest

from investment_rebalancer.model.asset.etf import ETF


class ModelTest(unittest.TestCase):
    def test_invalid_isin(self):
        with self.assertRaises(ValueError) as cm:
            ETF(isin="1234", name="test etf", current_price=1.0, ter=0.1)
        self.assertTrue("1234 is not a valid ISIN!" in str(cm.exception))

    def test_value_calculation(self):
        quantity = random.randint(1, 99)
        etf = ETF(
            isin="LU1781541179",
            name="test etf",
            quantity=quantity,
            ter=0.1,
            classifications={},
            enabled=True,
        )
        self.assertEqual(etf.current_price * quantity, etf.current_value)

    def test_equals(self):
        quantity = random.randint(1, 99)
        etf1 = ETF(
            isin="LU1781541179",
            name="test etf",
            quantity=quantity,
            ter=0.1,
            classifications={},
            enabled=True,
        )
        etf2 = ETF(
            isin="LU1781541179",
            name="test etf",
            quantity=quantity,
            ter=0.1,
            classifications={},
            enabled=True,
        )
        self.assertEqual(etf1, etf2)

        etf1 = ETF(
            isin="LU1781541179",
            name="test etf",
            quantity=quantity,
            ter=0.1,
            classifications={},
            enabled=True,
        )
        etf2 = ETF(
            isin="LU0635178014",
            name="test etf",
            quantity=quantity,
            ter=0.1,
            classifications={},
            enabled=True,
        )
        self.assertNotEqual(etf1, etf2)
