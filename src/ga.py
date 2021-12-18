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
import copy


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
        print("initialized population: ", self.population)
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
            # print(type(P1.number_of_lines).__name__, type(P2).__name__)
            if len(P1) >= len(P2):
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
            # self.population.append(P1)

            if len(P1) >= len(P2):
                return P1
            else:
                return P2

    def crossover(self, parent1, parent2):
        alpha = random.random()
        # Copy parent's information
        limit_suite = parent1.limit_suite
        limit_test = parent1.limit_test
        module = parent1.module
        module_path = parent1.module_path
        sut_info = parent1.sut_info
        number = parent1.number

        # Create child test suites
        O1 = testsuite.TestSuite(
            limit_suite, limit_test, (module, module_path), sut_info, number)
        O2 = testsuite.TestSuite(
            limit_suite, limit_test, (module, module_path), sut_info, number)

        O1.test_cluster = parent1.test_cluster[:round(alpha * (len(parent1)))] + \
            parent2.test_cluster[round((1 - alpha) * (len(parent2))):]
        O2.test_cluster = parent2.test_cluster[:round(alpha * (len(parent2)))] + \
            parent1.test_cluster[round((1 - alpha) * (len(parent1))):]

        return O1, O2

    def mutate(self, offspring: testsuite.TestSuite):

        mutationType = {
            0: "Modify",
            1: "Add",
            2: "Delete"
        }

        for testcase in offspring.test_cluster:
            if len(testcase.statement_list) < 2:
                continue
            elif random.random() < (1 / len(offspring)):
                # mutation_type = mutationType[random.randint(0, 2)]
                # if (mutation_type == "Delete" or mutation_type == "Modify"):
                print("Before: ", testcase.statement_list)
                 statement_idx = random.randint(
                      1, len(testcase.statement_description) - 1)
                  statement = testcase.statement_description[statement_idx]
                   if (mutation_type == "Delete"):
                        self.delete_statement(statement, test)
                    else:
                        self.mutate_statement(
                            statement_idx, statement, testcase)

                    print("After: ", testcase.statement_list)
                else:
                testcase.make_statement()
                print("After: ", testcase.statement_list)

        return offspring

    # def delete_statement(self, statement, testcase):

    def mutate_statement(self, index, statement, testcase):
        print("Statement: ", statement.statement)
        statement_type = type(statement).__name__
        if statement_type == "PrimitiveStatement":
            statement.generate_random_value()
            statement.generate_statement()
            print('Statement_orimitive: ', statement.statement)
            print('Testcase: ', testcase.statement_list)
            testcase.statement_list[index] = statement.statement
        elif statement_type == "ConstructorStatement" or statement_type == "FunctionStatement" or statement_type == "MethodStatement":
            arg_list = statement.arg_list
            mutate_list = []
            for i, d in enumerate(testcase.statement_description):
                if type(d).__name__ == "ImportStatement":
                    continue
                if d.statement_variable in arg_list:
                    mutate_list.append((i, d))
            for s in mutate_list:
                self.mutate_statement(s[0], s[1], testcase)
            statement.generate_statement()

    def calculate_fitnesses(self):
        current_best = []
        for testsuit in self.population:
            testsuit.find_suite_coverage(self.output_folder_path)

    def run_ga(self, epochs):
        self.initialize_population()
        self.calculate_fitnesses()
        current_best = []
        for i in range(epochs):

            while len(self.population) <= 2*(self.population_size):
                p1 = self.selection()
                p2 = self.selection()
                P1 = copy.deepcopy(p1)
                P2 = copy.deepcopy(p2)
                print("P1: ", type(P1).__name__)
                alpha = random.random()
                gamma = random.random()
                while P1 == P2:
                    P1 = self.selection()
                if alpha < self.crossover_rate:
                    O1, O2 = self.crossover(P1, P2)
                    print("O1: ", type(O1).__name__)
                else:
                    O1, O2 = P1, P2

                if gamma < self.mutation_rate:
                    self.mutate(O1)
                    self.mutate(O2)
                self.population.append(O1)
                self.population.append(O1)
            print("Population: ", self.population)
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
