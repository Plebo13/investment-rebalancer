import unittest

from investment_rebalancer.model.asset.FlatAsset import FlatAsset


class FlatAssetTest(unittest.TestCase):
    def test_constructor(self):
        name = "test_name"
        target_allocation = 50.0
        named = FlatAsset(name, target_allocation)
        self.assertEqual(named.current_value, 0.0)


if __name__ == '__main__':
    unittest.main()
