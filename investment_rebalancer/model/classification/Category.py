from investment_rebalancer.model.Named import Named


class Category(Named):

    def __init__(self, name: str, target_allocation: float):
        """
        Constructor for a given name and a given allocation.
        :param name: the name of the asset
        :param target_allocation: the allocation for that asset
        """
        super().__init__(name)
        self.target_allocation = target_allocation
        self.current_allocation = 0.0
        self.current_value = 0.0
        self.delta_value = 0.0
        self.investment_value = 0.0

    def __eq__(self, other: object) -> bool:
        """
        Checks whether or not an object is equal to this instance.
        Two categories are equal if they have the same name.
        :param other: the other object
        :return: true if the other object is equal, otherwise false
        """
        if other == self:
            return True
        if not isinstance(other, Category):
            return False
        return other.name == self.name

    def __str__(self) -> str:
        """
        Creates a string with the classifications name and its investment value.
        :return: the string
        """
        return self.name + ": " + str(self.investment_value) + "€"
