from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractTestcase(ABC):

    def __init__(self):
        self.statement_list = []

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_type') and
                callable(subclass.get_type) and
                hasattr(subclass, 'get_value') and
                callable(subclass.get_value) or
                NotImplemented)

    @classmethod
    @abstractmethod
    def generate_random_testcase(cls, *args):

        """
        generates random
        :param args: need some info about module
        :return: the new testcase
        """

