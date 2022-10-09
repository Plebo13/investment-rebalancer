import unittest

from main.model import configuration
from main.model.errors import ConfigurationException


class ConfigurationTest(unittest.TestCase):
    def test_config_does_not_exist(self):
        config_path = "tests/test_configs/invalid.json"
        with self.assertRaises(ConfigurationException) as cm:
            configuration.parse(config_path)
        self.assertEquals(
            f"The given configuration file does not exist: {config_path}", str(cm.exception)
        )

    def test_missing_key(self):
        config_path = "tests/test_configs/missing_key.json"
        with self.assertRaises(ConfigurationException) as cm:
            configuration.parse(config_path)
        self.assertEquals(
            "Key 'enabled' missing in ETF LU0635178014!", str(cm.exception)
        )

    def test_no_etfs(self):
        config_path = "tests/test_configs/no_etfs.json"
        with self.assertRaises(ConfigurationException) as cm:
            configuration.parse(config_path)
        self.assertEquals("No ETFs configured!", str(cm.exception))

    def test_valid_parsing(self):
        config_path = "tests/test_configs/valid.json"
        configuration.parse(config_path)
        self.assertEqual(
            2,
            len(configuration.etfs),
            "The list of ETFs does not have the correct length!",
        )
        self.assertEqual(
            "Lyxor Core MSCI World",
            configuration.etfs["LU1781541179"].name,
            "The name does not match the ID!",
        )
        self.assertEqual(
            "Lyxor MSCI Emerging Markets",
            configuration.etfs["LU0635178014"].name,
            "The name does not match the ID!",
        )


if __name__ == "__main__":
    unittest.main()
