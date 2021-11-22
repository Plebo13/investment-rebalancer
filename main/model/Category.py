from main.model.Named import Named


class Category(Named):

    def __init__(self, name: str, percentage: float) -> None:
        super().__init__(name)
        self.percentage = percentage
        self.current_percentage = 0.0
        self.current_value = 0.0
        self.delta_value = 0.0
        self.investment_value = 0.0

    def __eq__(self, o: object) -> bool:
        if o == self:
            return True
        if not isinstance(o, Category):
            return False
        return o.name == self.name

    def __str__(self) -> str:
        return self.name + ": " + str(self.investment_value) + "€"
