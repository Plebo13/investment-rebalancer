from main.model.Named import Named


class Category(Named):

    def __init__(self, name: str, percentage: float):
        """
        Constructor for a given name and a given allocation.
        :param name: the name of the asset
        :param percentage: the allocation for that asset
        """
        super().__init__(name)
        self.percentage = percentage
        self.allocation = 0.0
        self.current_value = 0.0
        self.delta_value = 0.0
        self.investment_value = 0.0

    def __eq__(self, o: object) -> bool:
        """
        Checks whether or not an object is equal to this instance.
        Two categories are equal if they have the same name.
        :param o: the other object
        :return: true if the other object is equal, otherwise false
        """
        if o == self:
            return True
        if not isinstance(o, Category):
            return False
        return o.name == self.name

    def __str__(self) -> str:
        """
        Creates a string with the classifications name and its investment value.
        :return: the string
        """
        return self.name + ": " + str(self.investment_value) + "€"
