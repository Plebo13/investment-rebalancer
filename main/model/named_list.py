from typing import List, TypeVar
from main.model.named import Named

T = TypeVar('T', bound=Named)


class NamedList(List[T]):
    def contains(self, name: str) -> bool:
        for element in self:
            if element.name == name:
                return True

        return False

    def get(self, name: str) -> T:
        for element in self:
            if element.name == name:
                return element
        raise ValueError("The given element is not in that list!")
