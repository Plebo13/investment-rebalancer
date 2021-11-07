from main.model.Category import Category
from main.model.Named import Named
from typing import List


class Classification(Named):
    def __init__(self, name: str):
        super().__init__(name)
        self.categories: List[Category] = []

    def __eq__(self, o: object) -> bool:
        if o == self:
            return True
        if not isinstance(o, Classification):
            return False
        return o.name == self.name

    def __str__(self) -> str:
        result = self.name
        for category in self.categories:
            result += "\n    "+str(category)
        return result
