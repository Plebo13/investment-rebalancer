from dataclasses import dataclass


@dataclass(eq=False)
class ETF:
    id: str
    name: str
    enabled: bool
    quantity: float
    ter: float
    investment: float = 0.0

    def __eq__(self, other: object) -> bool:
        if other == self:
            return True
        if not isinstance(other, ETF):
            return False
        return other.id == self.id
