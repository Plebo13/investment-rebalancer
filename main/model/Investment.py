from functools import total_ordering


@total_ordering
class Investment:
    name: str
    isin: str
    quantity: float
    price: float
    investment_sum: float
    __current_value: float
    categories: list

    def __init__(self, isin: str, name: str, quantity: float, price: float) -> None:
        self.isin = isin
        self.name = name
        self.quantity = quantity
        self.price = price
        self.__current_value = quantity * price

    def __str__(self):
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Investment):
            return False
        if other == self:
            return True

        return other.isin == self.isin

    def __lt__(self, other) -> bool:
        return self.__current_value > other.__current_value

    def add_category(self, category):
        self.categories.append(category)
