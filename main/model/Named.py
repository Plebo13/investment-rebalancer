from abc import ABC


class Named(ABC):
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, o: object) -> bool:
        if o == self:
            return True
        if not isinstance(o, Named):
            return False
        return o.name == self.name
