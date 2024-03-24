from typing import List

from pydantic import BaseModel, Field


class Category(BaseModel):
    name: str
    target_allocation: float
    current_allocation: float = Field(ge=0.0, default=0.0)
    delta_value: float = Field(default=0.0)
    to_invest: float = Field(ge=0.0, default=0.0)

    def __eq__(self, other: object) -> bool:
        """
        Checks whether or not an object is equal to this instance.
        Two categories are equal if they have the same name.
        :param other: the other object
        :return: true if the other object is equal, otherwise false
        """
        if not isinstance(other, Category):
            return False
        return other.name == self.name
