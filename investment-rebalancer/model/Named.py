from abc import ABC


class Named(ABC):
    def __init__(self, name: str):
        """
        Constructor with a given name.
        :param name: the name of the object
        """
        self.name = name

    def __eq__(self, o: object) -> bool:
        """
        Checks whether or not an object is equal to this instance.
        Two objects of this class are equal if they have the same name.
        :param o: the other object
        :return: true if the other object is equal, otherwise false
        """
        if o == self:
            return True
        if not isinstance(o, Named):
            return False
        return o.name == self.name
