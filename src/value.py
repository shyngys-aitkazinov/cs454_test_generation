from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractValue(ABC):

    def __init__(self, value, custom_type):
        self.value = value
        self.type = custom_type

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_type') and
                callable(subclass.get_type) and
                hasattr(subclass, 'get_value') and
                callable(subclass.get_value) or
                NotImplemented)

    @abstractmethod
    def get_value(self):
        """

        :return: encapsulated value
        """

    @abstractmethod
    def get_type(self):
        """

        :return: our customly defined type
        """


class Value(AbstractValue):

    def __init__(self, value, custom_type):
        super().__init__(value, custom_type)

    def get_value(self):
        return self.value

    def get_type(self):
        return self.type

