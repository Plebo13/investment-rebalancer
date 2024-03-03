import unittest

from pydantic import ValidationError

from investment_rebalancer.model import configuration


class ConfigurationTest(unittest.TestCase):
    def test_config_does_not_exist(self):
        config_path = "tests/test_configs/invalid.yml"
        with self.assertRaises(configuration.ConfigurationException) as cm:
            configuration.parse(config_path)
        self.assertEqual(
            f"The given configuration file does not exist: {config_path}",
            str(cm.exception),
        )

    def test_missing_key(self):
        config_path = "tests/test_configs/incomplete.yml"
        with self.assertRaises(ValidationError) as cm:
            configuration.parse(config_path)

    def test_valid_parsing(self):
        config_path = "tests/test_configs/valid.yml"
        config = configuration.parse(config_path)
        self.assertEqual(
            2,
            len(config.etfs),
            "The list of ETFs does not have the correct length!",
        )


if __name__ == "__main__":
    unittest.main()
