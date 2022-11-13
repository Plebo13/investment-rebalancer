class ETF:
    def __init__(
        self,
        isin: str,
        name: str,
        enabled: bool,
        quantity: float,
        current_price: float,
        ter: float,
    ) -> None:
        self.id = isin
        self.name = name
        self.enabled = enabled
        self.quantity = quantity
        self.current_value = quantity * current_price
        self.ter = ter
        self.investment: float = 0.0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ETF):
            return False
        return other.id == self.id
