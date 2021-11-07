class Category:
    name: str
    percentage: float
    investments = list()

    def __init__(self, name: str, percentage: float) -> None:
        self.name = name
        self.percentage = percentage

    def __eq__(self, o: object) -> bool:
        if o == self:
            return True
        if not isinstance(o, Category):
            return False
        return o.name == self.name

    def get_value(self) -> float:
        value = 0.0
        for investment in self.investments:
            value = value + investment.current_value
        return value
