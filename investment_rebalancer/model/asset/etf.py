import sharepp
from pydantic import BaseModel, Field, computed_field, field_validator


class ETF(BaseModel):
    isin: str
    name: str
    enabled: bool = Field(default=False)
    quantity: float = Field(default=0.0)
    current_price: float
    ter: float
    investment: float = Field(default=0.0)

    @computed_field
    @property
    def current_value(self) -> float:
        return self.quantity * self.current_price

    @field_validator("isin")
    @classmethod
    def name_must_contain_space(cls, isin: str) -> str:
        if not sharepp.is_isin(isin):
            raise ValueError(f"{isin} is not a valid ISIN!")
        return isin

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ETF):
            return False
        return other.isin == self.isin
