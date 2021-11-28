from abc import abstractmethod, ABC

from main.model.Named import Named


class AbstractAsset(Named, ABC):
    def __init__(self, name: str, percentage: float):
        """
        Constructor for a given name and a given allocation.
        :param name: the name of the asset
        :param percentage: the allocation for that asset
        """
        super().__init__(name)
        self.percentage = percentage
        self.current_value = 0.0
        self.delta_value = 0.0
        self.investment_value = 0.0

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def calculate_current_value(self):
        pass

    @abstractmethod
    def rebalance(self):
        pass

    def calculate_delta(self, total_value: float):
        """
        Calculates the delta value between the current value and the desired value based on the assets allocation.
        :param total_value: the new total value
        """
        self.delta_value = total_value * self.percentage / 100 - self.current_value

    @abstractmethod
    def print(self):
        pass
