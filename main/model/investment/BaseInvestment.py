from abc import ABC, abstractmethod

from main.model.named import Named


class BaseInvestment(Named, ABC):
    def __init__(self, enabled: bool, name: str, quantity: float, target_allocation: float = 0.0):
        super().__init__(name)
        self.enabled = enabled
        self.quantity = quantity
        self.current_value = 0.0
        self.investment_value = 0.0
        self.target_allocation = target_allocation

    def __lt__(self, other) -> bool:
        if self.target_allocation != 0 or other.target_allocation != 0:
            return self.target_allocation > other.target_allocation
        return self.current_value > other.current_value

    @abstractmethod
    def calculate_current_value(self):
        pass