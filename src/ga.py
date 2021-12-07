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
        # self.config = configuration
        self.sut_info = configuration["sut_info"]
        self.population_size = configuration["pop_size"]
        self.number_of_testsuit = configuration["number_of_testsuits"]
        self.mutation_rate = configuration["mutation_rate"]
        self.crossover_rate = configuration["crossover_rate"]
        self.module_name = configuration["module_name"]
        self.limit_suite = configuration["limit_suite"]
        self.limit_test = configuration["limit_test"]
        self.path = configuration["path"]
        self.population = []

    def initialize_population(self):
        # for i in range(self.population_size):
        for i in range(4):
            print(i)
            test_suite = testsuite.TestSuite(self.limit_suite, self.limit_test, self.module_name, self.sut_info)
            test_suite.generate_random_test_suite(self.path)
            self.population.append(test_suite)

        return

    def selection(self):
        if random.random() > 0.5:
            '''
            Tournament selection:
            '''
            P1 = self.population[int(random.random()* len(self.population))]
            P2 = self.population[int(random.random()* len(self.population))]

            while P1 == P2:
                P2 = self.population[int(random.random()* len(self.population))]
            if P1.number_of_lines >= P2.number_of_lines:
                return P1
            else:
                return P2
        else:
            '''
            Baised Roulette Wheel
            '''
            selector = random.random()
            for testsuite in  self.population:
                if (1/testsuite.number_of_lines) < selector:
                    P1 = testsuite
                    self.population.remove(testsuite)
            for testsuite in  self.population:
                if (1/testsuite.number_of_lines) < selector:
                    P2 = testsuite
            self.population.append(P1)

            if P1.number_of_lines >= P2.number_of_lines:
                return P1
            else:
                return P2



    def crossover(parent1, parent2):
        '''
        Needs to be updated
        '''
        alpha = random.random()
        O1 = parent1[:int(alpha(len(parent1)))] + parent2[int((1 - alpha)(len(parent2))):]
        O2 = parent2[:int(alpha(len(parent2)))] + parent1[int((1 - alpha)(len(parent1))):]
        return O1, O2

    def mutate(offsprining):
        if random.random() > (1 / len(offsprining)):
            # si = offsprining.pop(int(len(offsprining) * random.random()))
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

    # def fitness_evaluation(self):
    #     return int(20 * random.random())

    def run_ga(self, epochs):
        self.initialize_population()
        # print(self.population[0].test_cluster[0].fitness)
        current_best = []
        for testsuit in self.population:
            testsuit.find_suite_coverage()
            # print(testsuit.suite_coverage)
        for i in range(epochs):
            alpha = random.random()
            gamma = random.random()

            while len(self.population) <= 2(self.population_size):
                P1 = self.selection()
                P2 = self.selection()
                while P1==P2:
                    P1 = self.selection()
                if alpha > self.crossover_rate:
                    O1, O2 = self.crossover(P1, P2)
                else:
                    O1, O2 = P1, P2
                if gamma > self.mutation_rate:
                    self.mutate(O1)
                    self.mutate(O2)
                self.population.append(O1)
                self.population.append(O1)
            self.population.sort(key=lambda testsuit: testsuit.number_of_lines)
            for i in range(self.population_size):
                current_best.append(self.population[i])
            current_best.sort(key=lambda testsuit: testsuit.number_of_lines)
            current_best = current_best[:self.population_size]
            self.population = self.population[:self.population_size]
            '''
            #TODO: I will add stop condition if
                100 coverage reached 
            '''

        return


