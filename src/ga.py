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
import testcase as t
import copy
import time


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
        self.random_testcase_rate = configuration["random_testcase_rate"]

        self.module_name = configuration["module_name"][0]
        self.module_name_path = configuration["module_name"][1]
        self.limit_suite = configuration["limit_suite_testcases"]
        self.limit_test = configuration["limit_test_lines"]
        self.output_folder_path = configuration["output_folder_path"]
        self.selection_type = configuration["selection"]
        self.population = []
        self.stats = {
            "average fitness": [],
            "best fitness": []
        }
        self.normalized_fitness = 1.0

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
            if random.random() > 0.2:

                P1 = self.population[int(
                    random.random() * len(self.population)*0.2)]
                return P1
            else:

                P1 = self.population[int(
                    random.random() * len(self.population))]

                return P1

        elif self.selection_type == "roulette_wheel":
            '''
            Biased Roulette Wheel: not supported
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
        cut_off1 = int(alpha * (len(parent1)))
        cut_off2 = int(alpha * (len(parent2)))
        temp_list1 = parent1.test_cluster[:cut_off1] + \
            parent2.test_cluster[cut_off2:]
        temp_list2 = parent2.test_cluster[:cut_off2] + \
            parent1.test_cluster[cut_off1:]
        O1.test_cluster = temp_list1
        O2.test_cluster = temp_list2

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
                mutation_type = mutationType[random.randint(0, 2)]
                if (mutation_type == "Delete" or mutation_type == "Modify"):
                    # print("Before: ", testcase.statement_list)
                    statement_idx = random.randint(
                        1, len(testcase.statement_description) - 1)
                    statement = testcase.statement_description[statement_idx]
                    if mutation_type == "Delete":
                        self.delete_statement(statement, testcase)
                        # print("After deletion: ", testcase.statement_list)
                    else:
                        self.mutate_statement(
                            statement_idx, statement, testcase)

                        # print("After modify: ", testcase.statement_list)
                else:
                    testcase.make_statement()
                    # print("After add: ", testcase.statement_list)

        return offspring

    def mutate_statement(self, index, statement, testcase):
        statement_type = type(statement).__name__
        if statement_type == "PrimitiveStatement":
            statement.generate_random_value()
            statement.generate_statement()
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

    def delete_statement(self, statement, testcase):
        statement_kind = type(statement).__name__
        statement_type = statement.statement_type
        statement_variable = statement.statement_variable
        occurences = []
        replacements = []
        index = testcase.statement_description.index(statement)

        # If the statement to delete is the last one
        if index == len(testcase.statement_description) - 1:
            testcase.statement_list.remove(statement.statement)
            testcase.statement_description.pop()
            return
        # Find occurences of the statement variable
        for idx, st in enumerate(testcase.statement_description[index + 1:]):
            if type(st).__name__ == "PrimitiveStatement":
                continue

            if type(st).__name__ == "MethodStatement" and st.obj == statement_variable and statement_variable not in st.arg_list:
                occurences.append((idx + index + 1, [], st))

            if statement_variable in st.arg_list:
                v_idx = []
                for i, arg in enumerate(st.arg_list):
                    if arg == statement_variable:
                        v_idx.append(i)
                occurences.append((idx + index + 1, v_idx, st))

        # Find replacements from before
        for idx, st in enumerate(testcase.statement_description[:index]):
            if type(st).__name__ == statement_kind and st.statement_type == statement_type:
                replacements.append(st)

        # print("Occurences: ", occurences)
        # print("Replacements: ", replacements)

        if len(replacements) > 0:
            for idx, v_idx, st in occurences:
                old_st = st.statement
                if type(st).__name__ == "MethodStatement":
                    replacement = random.choice(replacements)
                    st.obj = replacement.statement_variable
                for j in v_idx:
                    replacement = random.choice(replacements)
                    st.arg_list[j] = replacement.statement_variable
                st.generate_statement()
                i = testcase.statement_list.index(old_st)
                testcase.statement_list[i] = st.statement
        else:
            for idx, v_idx, st in occurences:
                self.delete_statement(st, testcase)
        # print("to remove: ", statement.statement)
        testcase.statement_list.remove(statement.statement)
        testcase.statement_description.remove(statement)

    def calculate_fitnesses(self, statistics):
        all_fitnesses = []
        for testsuit in self.population:
            suite_fitness = testsuit.find_suite_coverage(
                self.output_folder_path)
            all_fitnesses.append(suite_fitness / self.normalized_fitness)

        best = max(all_fitnesses)
        ave = sum(all_fitnesses) / len(all_fitnesses)
        statistics["average fitness"].append(ave)
        statistics["best fitness"].append(best)

    def clean_suite(self):
        for testsuite in self.population:
            for i in range(len(testsuite.test_cluster) - 1, -1, -1):
                if len(testsuite.test_cluster[i].statement_list) < 2:
                    testsuite.test_cluster.pop(i)

        for testsuite in self.population[:]:
            if len(testsuite) == 0:
                self.population.remove(testsuite)

    def reassign_suite_numbers(self):
        for i in range(len(self.population)):
            self.population[i].number = i

    def initialize_coverage(self):
        testcase = t.Testcase(
            (self.module_name, self.module_name_path), self.sut_info, 0)
        testcase.generate_random_testcase()
        data, err = testcase.find_coverage(self.output_folder_path)
        if data is not None:

            if 'missing_lines' in data and 'summary' in data:
                self.normalized_fitness = len(
                    data['missing_lines']) / data['summary']['num_statements']
                print("Missing lines: ", len(data['missing_lines']),
                      "Total lines: ", data['summary']['num_statements'])
                if self.normalized_fitness == 0:
                    self.normalized_fitness = 1
                print("Normalized coverage", self.normalized_fitness)

    def run_random_search(self, epochs):
        stats = {
            "average fitness": [],
            "best fitness": [],
            "max": []
        }
        for e in range(epochs):
            self.population = []

            for i in range(self.population_size):
                test_suite = testsuite.TestSuite(self.limit_suite, self.limit_test,
                                                 (self.module_name, self.module_name_path), self.sut_info, i)
                test_suite.generate_random_test_suite(self.output_folder_path)
                self.population.append(test_suite)
            self.calculate_fitnesses(stats)

            if e == 0:
                stats["max"].append(stats["best fitness"][-1])
            else:
                stats["max"].append(
                    max(stats["best fitness"][-1], stats["max"][-1]))

        return stats

    def save_testsuites(self):

        for test_suite in self.population:
            test_suite.write_test_suite(self.output_folder_path)

    def run_ga(self, epochs):
        self.initialize_population()
        self.initialize_coverage()

        for i in range(epochs):
            print(f"**************   Start of {i} epoch     ***********")
            self.calculate_fitnesses(self.stats)
            while len(self.population) <= 2*(self.population_size):
                P1 = self.selection()
                P2 = self.selection()

                alpha = random.random()
                gamma = random.random()

                while P1 == P2:
                    P1 = self.selection()
                # print(P1, P2)
                P1 = copy.deepcopy(P1)
                P2 = copy.deepcopy(P2)
                # print(P1, P2)
                if alpha < self.crossover_rate:
                    O1, O2 = self.crossover(P1, P2)
                else:
                    O1, O2 = P1, P2

                if gamma < self.mutation_rate:
                    self.mutate(O1)
                    self.mutate(O2)

                # random test generation
                if len(O1) < self.limit_suite:
                    delta = random.random()
                    if delta < self.random_testcase_rate:
                        O1.generate_random_testcase(self.output_folder_path)
                if len(O2) < self.limit_suite:
                    delta = random.random()
                    if delta < self.random_testcase_rate:
                        O2.generate_random_testcase(self.output_folder_path)

                O1.find_suite_coverage(self.output_folder_path)
                O2.find_suite_coverage(self.output_folder_path)
                self.population.append(O1)
                self.population.append(O1)

            self.population.sort(
                key=lambda testsuit: testsuit.suite_fitness, reverse=True)
            self.population = self.population[:self.population_size]

            # cleaning
            self.clean_suite()
            self.reassign_suite_numbers()

            # reassign
            while(len(self.population) < self.population_size):
                test_suite = testsuite.TestSuite(self.limit_suite, self.limit_test,
                                                 (self.module_name, self.module_name_path), self.sut_info, len(self.population_size))
                test_suite.generate_random_test_suite(self.output_folder_path)
                self.population.append(test_suite)

        print("Stats: ", self.stats)
        self.save_testsuites()


        return self.stats
