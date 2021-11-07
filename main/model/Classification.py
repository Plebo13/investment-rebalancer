from main.model.Category import Category


class Classification:
    categories = list()

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, o: object) -> bool:
        if o == self:
            return True
        if not isinstance(o, Classification):
            return False
        return o.name == self.name

    def get_value(self) -> float:
        value = 0.0
        for category in self.categories:
            assert isinstance(category, Category)
            value = value + category.get_value()
        return value
