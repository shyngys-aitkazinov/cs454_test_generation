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
import testsuite


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


class GA():
    def __init__(self, configuration):

        self.sut_info = configuration["sut_info"]
        self.population_size = configuration["pop_size"]
        self.mutation_rate = configuration["mutation_rate"]
        self.crossover_rate = configuration["crossover_rate"]
        self.module_name = configuration["module_name"][0]
        self.module_name_path = configuration["module_name"][1]
        self.limit_suite = configuration["limit_suite_testcases"]
        self.limit_test = configuration["limit_test_lines"]
        self.output_folder_path = configuration["output_folder_path"]
        self.selection_type = configuration["selection"]
        self.population = []

    def initialize_population(self):
        for i in range(self.population_size):
            test_suite = testsuite.TestSuite(self.limit_suite, self.limit_test,
                                             (self.module_name, self.module_name_path), self.sut_info, i)
            test_suite.generate_random_test_suite(self.output_folder_path)
            self.population.append(test_suite)
        return

    def selection(self):
        # if random.random() > 0.5:
        if self.selection_type == "tournament":
            '''
            Tournament selection:
            '''
            P1 = self.population[int(random.random() * len(self.population))]
            P2 = self.population[int(random.random() * len(self.population))]

            while P1 == P2:
                P2 = self.population[int(
                    random.random() * len(self.population))]
            print(type(P1.number_of_lines).__name__, type(P2).__name__)
            if P1.number_of_lines >= P2.number_of_lines:
                return P1
            else:
                return P2
        elif self.selection_type == "roulette_wheel":
            '''
            Biased Roulette Wheel
            '''
            selector = random.random()
            for testsuite in self.population:
                if (1/testsuite.number_of_lines) < selector:
                    P1 = testsuite
                    self.population.remove(testsuite)
            for testsuite in self.population:
                if (1/testsuite.number_of_lines) < selector:
                    P2 = testsuite
            self.population.append(P1)

            if P1.number_of_lines >= P2.number_of_lines:
                return P1
            else:
                return P2

    def crossover(self, parent1, parent2):
        '''
        Needs to be updated
        '''
        alpha = random.random()
        O1 = parent1.test_cluster[:round(alpha * (len(parent1)))] + \
            parent2.test_cluster[round((1 - alpha) * (len(parent2))):]
        O2 = parent2.test_cluster[:round(alpha * (len(parent2)))] + \
            parent1.test_cluster[round((1 - alpha) * (len(parent1))):]
        return O1, O2

    def mutate(self, offspring):

        mutationType = {
            0: "Modify",
            1: "Add",
            2: "Delete"
        }

        print("Offspring type: ", type(offspring).__name__)

        for testcase in offspring.test_cluster:
            if random.random() < (1 / len(offspring)):
                mutation_type = mutationType[random.randint(0, 2)]
                if (mutation_type == "Delete" or mutation_type == "Modify"):
                    statement_idx = random.randint(
                        1, len(testcase.statement_description) - 1)
                    statement = testcase.statement_description[statement_idx]
                    if (mutation_type == "Delete"):
                        pass
                    else:
                        self.mutate_statement(statement)
                        testcase.statement_list[statement_idx] = statement.statement
                        # elif statement_type == "ConstructorStatement":

                        # elif statement_type == "FunctionStatement":
                        #     arg_statement_list = []
                        #     for i in testcase.statement_description:
                        #         if i.statement_variable in statement.arg_list:
                        #             typ = i.statement_type
                else:
                    testcase.make_statement()

        return offspring

    def mutate_statement(self, statement):
        statement_type = type(statement).__name__
        if statement_type == "PrimitiveStatement":
            statement.generate_random_value()
            statement.generate_statement()
        # elif statement_type == "ConstructorStatement":

    def calculate_fitnesses(self):
        current_best = []
        for testsuit in self.population:
            testsuit.find_suite_coverage(self.output_folder_path)

    def run_ga(self, epochs):
        self.initialize_population()
        # print(self.population[0].test_cluster[0].fitness)
        self.calculate_fitnesses()
        current_best = []
        # print(testsuit.suite_coverage)
        for i in range(epochs):

            while len(self.population) <= 2*(self.population_size):
                P1 = self.selection()
                P2 = self.selection()
                alpha = random.random()
                gamma = random.random()
                while P1 == P2:
                    P1 = self.selection()
                if alpha < self.crossover_rate:
                    O1, O2 = self.crossover(P1, P2)
                else:
                    O1, O2 = P1, P2
                if gamma < self.mutation_rate:
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
