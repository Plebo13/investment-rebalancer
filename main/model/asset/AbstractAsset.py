from abc import abstractmethod, ABC

from main.model.Named import Named


class AbstractAsset(Named, ABC):
    def __init__(self, name: str, percentage: float):
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
        self.delta_value = total_value * self.percentage / 100 - self.current_value

    @abstractmethod
    def print(self):
        pass
