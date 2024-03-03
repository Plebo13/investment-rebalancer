from functools import cached_property
from typing import Dict

import sharepp
from pydantic import BaseModel, Field, computed_field, field_validator


class ETF(BaseModel):
    isin: str
    name: str
    enabled: bool
    quantity: float
    ter: float
    classifications: Dict[str, str]
    investment: float = Field(default=0.0)

    @computed_field
    @cached_property
    def current_price(self) -> float:
        return sharepp.get_etf_price(self.isin)

    @computed_field
    @property
    def current_value(self) -> float:
        return self.quantity * self.current_price

    @field_validator("isin")
    @classmethod
    def validate_isin(cls, isin: str) -> str:
        if not sharepp.is_isin(isin):
            raise ValueError(f"{isin} is not a valid ISIN!")
        return isin

    def __eq__(self, other: object) -> bool:
        """Checks whether or not an object is equal to this instance.
        Two ETF's are equal if they have the same ISIN.
        :param other: the other object
        :return: true if the other object is equal, otherwise false
        """
        if not isinstance(other, ETF):
            return False
        return other.isin == self.isin
