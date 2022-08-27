import unittest

from main.model.configuration import Configuration
from main.model.errors import ConfigurationException


class ConfigurationTest(unittest.TestCase):
    def test_config_does_not_exist(self):
        config_path = "tests/test_configs/invalid.json"
        with self.assertRaises(ConfigurationException) as cm:
            Configuration(config_path)
            self.assertEquals(
                f"The given configuration does not exist: {config_path}",
                str(cm.exception),
            )

    def test_valid_parsing(self):
        config_path = "tests/test_configs/70-30.json"
        config = Configuration(config_path)
        config.parse()
        self.assertEqual(
            2, len(config.etfs), "The list of ETFs does not have the correct length!"
        )
        self.assertEqual(
            "LU1781541179",
            config.etfs[0].id,
            "The first entry does not have the expected ID!",
        )
        self.assertEqual(
            "Lyxor Core MSCI World",
            config.etfs[0].name,
            "The first entry does not have the expected name!",
        )


if __name__ == "__main__":
    unittest.main()
