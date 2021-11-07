from main.model.Named import Named


class Classification(Named):
    categories = list()

    def __init__(self, name: str):
        super().__init__(name)

    def __eq__(self, o: object) -> bool:
        if o == self:
            return True
        if not isinstance(o, Classification):
            return False
        return o.name == self.name
