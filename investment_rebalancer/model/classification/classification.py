from typing import Dict

from pydantic import BaseModel

from investment_rebalancer.model.classification.category import Category


class Classification(BaseModel):
    key: str
    name: str
    categories: Dict[str, Category]

    def __eq__(self, other: object) -> bool:
        """
        Checks whether or not an object is equal to this instance.
        Two classifications are equal if they have the same name.
        :param other: the other object
        :return: true if the other object is equal, otherwise false
        """
        if not isinstance(other, Classification):
            return False
        return self.name == other.name
