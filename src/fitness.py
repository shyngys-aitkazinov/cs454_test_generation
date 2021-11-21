from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractFitness(ABC):

    @classmethod
    def initialize_fitness_parameters(cls, *args, **kwargs):
        """initialize necessary parameters for further fitness computations"""
        pass

    @staticmethod
    @abstractmethod
    def calculate_fitness(*args, **kwargs):
        """
        Design and calculate the fitness of testcase/testsuite. feel free to add parameters
        :param args:
        :param kwargs:
        :return: single value
        """


