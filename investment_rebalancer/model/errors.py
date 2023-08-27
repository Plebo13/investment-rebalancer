class ConfigurationException(BaseException):
    pass


class IsinConfigurationException(ConfigurationException):
    def __init__(self, security_name: str, *args: object) -> None:
        super().__init__(*args)
        self.security_name = security_name

    pass
