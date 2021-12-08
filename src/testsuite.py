import testcase as t
import os
import sys
from pathlib import Path
import random
from typing import Tuple


class TestSuite(object):
    def __init__(self, limit_suite, limit_test, module: Tuple[str, str], sut_info, number=0):
        self.test_cluster = []
        self.limit_suite = limit_suite
        self.limit_test = limit_test
        self.module = module[0]   # name
        self.module_path = module[1]  # relative path
        self.sut_info = sut_info
        self.suite_coverage = []
        self.number = number
        # number of lines covered by the testsuite
        self.number_of_lines = 0

    # def delete_testuite(self):

    def __len__(self):
        return len(self.test_cluster)

    def generate_random_test_suite(self, output_folder_path='.'):

        random_num_testcases = random.randint(1, self.limit_suite + 1)
        for i in range(random_num_testcases):
            # (self, module: Tuple[str, str], test_cluster: parse.TestCluster, limit, timeout_time=5):
            testcase = t.Testcase(
                (self.module, self.module_path), self.sut_info, self.limit_test)
            testcase.generate_random_testcase()
            self.test_cluster.append(testcase)

        # print(self.test_cluster)
        self.write_test_suite(output_folder_path)

        return

    def write_test_suite(self, output_folder_path='.'):
        # writes the whole test suite into the file
        folder_name = "testsuite_" + self.module + f"_{self.number}"
        folder_path = output_folder_path
        path = os.path.join(folder_path, folder_name)
        count = 0
        # print(str(path))
        if not os.path.exists(path):
            os.mkdir(path)

        for testcase in self.test_cluster:
            test_name = "test_" + str(count) + ".py"
            p = os.path.join(path, test_name)
            f = open(p, "w+")
            # print(testcase.statement_list)
            for statement in testcase.statement_list:
                f.write(statement + "\n")
            f.close()
            count += 1

    def find_suite_coverage(self, output_folder_path="."):
        """
        returns line covered by the testsuit, union of each  test case line coverage:
        """
        total_number = 0
        self.suite_coverage = []

        for test in self.test_cluster:
            fitness, executed_lines, total_number_of_lines = test.find_fitness(
                output_folder_path)
            total_number = max(total_number_of_lines, total_number)
            if fitness > 0:
                self.suite_coverage = list(
                    set(self.suite_coverage) | set(executed_lines))
        self.suite_coverage.sort()
        self.number_of_lines = len(self.suite_coverage)

        if total_number > 0:
            print("Suite coverage:", len(self.suite_coverage) / total_number)
            return len(self.suite_coverage) / total_number
        print("Suite coverage:", len(self.suite_coverage))

        return len(self.suite_coverage)
