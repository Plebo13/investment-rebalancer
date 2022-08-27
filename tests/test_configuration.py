import unittest

from main.model.Configuration import Configuration
from main.model.exception.ConfigurationException import ConfigurationException


class ConfigurationTest(unittest.TestCase):
    def test_config_does_not_exist(self):
        config_path = "test_configs/invalid.json"
        with self.assertRaises(ConfigurationException) as cm:
            Configuration(config_path)
            self.assertEquals(
                f"The given configuration does not exist: {config_path}",
                str(cm.exception),
            )


if __name__ == "__main__":
    unittest.main()
