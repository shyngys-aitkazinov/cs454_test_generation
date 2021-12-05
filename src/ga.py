from __future__ import annotations
# from abc import ABC, abstractmethod
from array import array
from tokenize import String
import string
import random
# from typing_extensions import Unpack
from parse import *
from inspect import *
from testcase import *


class AbstractGA(ABC):

    def __init__(self, configuration):
        self.config = configuration
        # depending on configuration, we might tune the initial_parameters

    @abstractmethod
    def initialize_population(self, module_representation):
        """
        creates the initial population
        :param self:
        :param module_representation:
        :return: initial population
        """

    @abstractmethod
    def selection(self):
        """
        select individual for mating pool
        :param self:
        :return:
        """

    @abstractmethod
    def crossover(self):
        """
        implement crossover operation
        :param self:
        :return:
        """

    @abstractmethod
    def crossover_individuals(self, ind1, ind2):
        """
        performs crossover over single individuals
        :param ind1:
        :param ind2:
        :return:
        """

    @abstractmethod
    def mutate(self):
        """
        performs mutation of the individuals
        :param self:
        :return:
        """

    @abstractmethod
    def mutate_individual(self, individual):
        """
        performs mutation of single individual
        :param individual:
        :param self:
        :return:
        """

    @abstractmethod
    def fitness_evaluation(self):
        """
        performs fitness evaluation on the population
        :return:
        """

    @abstractmethod
    def run_ga(self, epochs):
        """
        perform a full cycle of gas until termination conditions
        :param epochs:
        :return:
        """


class GA(AbstractGA):
    def __init__(self, configuration):
        self.config = configuration

    def initialize_population(self, module_representation):
        pop = [FunctionTestcase(module_representation, module_representation.name).generate_random_testcase() for _ in
               range(10)]
        # print(pop)
        return pop

    def selection(self):
        return super().selection()

    def crossover(parent1, parent2):
        alpha = random.random()
        O1 = parent1[:int(alpha(len(parent1)))] + parent2[int((1 - alpha)(len(parent2))):]
        O2 = parent2[:int(alpha(len(parent2)))] + parent1[int((1 - alpha)(len(parent1))):]
        return O1, O2

    def mutate(offsprining):
        if random.random() > (1 / len(offsprining)):
            si = offsprining.pop(int(len(offsprining) * random.random()))
            '''
            #TODO: find value of si and
            # if possible find a way to replace si with the same type
            '''
        if random.random() > (1 / len(offsprining)):
            ...
        return offsprining

    def crossover_individuals(self):
        return super().crossover_individuals()

    def mutate_individual(self):
        return super().mutate_individual()

    def fitness_evaluation(self):
        return int(20 * random.random())

    def run_ga(self, epochs):
        current_population = self.initialize_population(self.config)
        print(current_population[1][1][0])
        fitness = dict()
        for i in range(10):
            fitness[self.fitness_evaluation()] = current_population[i]
        print(fitness)

        for i in range(epochs):
            # Z = max(fitness, key=fitness.get())
            # Z = [10, 24,56]
            # while len(Z) != len(current_population):
            #     P1 =  max(fitness, key=fitness.get())
            #     del fitness[P1]
            #     P2 =  max(fitness, key=fitness.get())
            #     del fitness[P2]
            #     O1, O2 = self.crossover(P1,P2)
            #     O1, O2 = self.mutate(O1), self.mutate(O2)
            #     fitness_parent = min(self.fitness_evaluation(P1), self.fitness_evaluation(P2))
            #     finess_offspring = min(self.fitness_evaluation(O1), self.fitness_evaluation(O2))
            #     length_parent = len(P1) + len(P2)
            #     length_offspring = len(O1) + len(O2)
            #     TB = ...

            pass
        return super().run_ga()

    pass


