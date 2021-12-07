from __future__ import annotations
import utils
from abc import ABC, abstractmethod
import random
import string
import parse
import os
from pathlib import Path
from statement import *
import json
from typing import Tuple
from threading import Lock
globallock = Lock()


class AbstractTestcase(ABC):

    def __init__(self):
        self.statement_list = []

    @classmethod
    @abstractmethod
    def generate_random_testcase(cls, *args):
        """
        generates random
        :param args: need some info about module
        :return: the new testcase
        """


class Testcase(AbstractTestcase):

    def __init__(self, module: Tuple[str, str], test_cluster: parse.TestCluster, limit, timeout_time=5):
        self.module_name = module[0]
        self.module_path = module[1]
        self.count = 0
        self.statement_list = []
        self.statement_description = []
        self.modifiers = test_cluster.modifiers
        self.generators = test_cluster.generators
        self.objects_under_test = test_cluster.objects_under_test
        self.limit = limit
        self.timeout_time = timeout_time
        self.fitness = 0
        self.executed_lines = []
        self.total_num_statements = 0

    def generate_random_testcase(self):
        # Add import statement
        import_statement = ImportStatement(self.module_name)
        import_statement.generate_statement()
        self.statement_description.append(import_statement)
        self.statement_list.append(import_statement.statement)

        random_length = random.randint(1, self.limit + 1)

        # Retrieve objects_under_test randomly and make corresponding statements
        while (len(self.objects_under_test) > 0 and len(self.statement_list) < random_length):
            self.make_statement()

    def make_statement(self):
        test_obj = random.choice(list(self.objects_under_test))
        test_obj_type = type(test_obj).__name__

        if test_obj_type == "Function":
            self.make_function(test_obj)

        elif test_obj_type == "Constructor":
            self.make_constructor(test_obj)

        elif test_obj_type == "Method":
            klass = test_obj.klass
            constr_statement = self.find_statement(klass)

            if constr_statement is not None:
                obj_name = constr_statement.statement_variable
            else:
                constructor_obj = list(self.generators[klass])[0]
                obj_name = self.generate_variable_name()
                self.make_constructor(constructor_obj, obj_name)
            self.make_method(test_obj, obj_name)

    def find_fitness(self, output_folder_path='.'):

        coverage, runtime_error = self.find_coverage(output_folder_path)

        if coverage is None:
            self.fitness = 0
            self.executed_lines = []
        elif runtime_error:
            self.fitness = 0
        else:
            self.fitness = coverage['summary']['percent_covered']
            self.executed_lines = coverage['executed_lines']
            self.total_num_statements = coverage['summary']['num_statements']

        return self.fitness, self.executed_lines, self.total_num_statements

    def make_method(self, test_obj, obj_name):
        arg_list = []
        # print("Mtype is ", test_obj.mtype[1])
        for _, value in test_obj.mtype[1].items():
            statement = self.find_statement(value)
            if statement is not None:
                var_name = statement.statement_variable

            elif self.is_primitive(value):
                var_name = self.generate_variable_name()
                statement = PrimitiveStatement(value, var_name)
                statement.generate_statement()

                self.statement_description.append(statement)
                self.statement_list.append(statement.statement)
            else:
                var_name = self.generate_variable_name()
                obj = list(self.generators[value])[0]
                self.make_constructor(obj, var_name)
            arg_list.append(var_name)

        method_var = self.generate_variable_name()
        method_statement = MethodStatement(
            test_obj.mtype, test_obj.method_name, test_obj.method, obj_name, arg_list, method_var)
        method_statement.generate_statement()
        self.statement_description.append(method_statement)
        self.statement_list.append(method_statement.statement)

    def make_function(self, test_obj):
        arg_list = []
        for _, value in test_obj.ftype[1].items():
            statement = self.find_statement(value)
            if statement is not None:
                var_name = statement.statement_variable

            elif self.is_primitive(value):
                var_name = self.generate_variable_name()
                statement = PrimitiveStatement(value, var_name)
                statement.generate_statement()
                self.statement_description.append(statement)
                self.statement_list.append(statement.statement)

            else:
                var_name = self.generate_variable_name()
                obj = list(self.generators[value])[0]
                self.make_constructor(obj, var_name)

            arg_list.append(var_name)

        func_var = self.generate_variable_name()
        func_statement = FunctionStatement(test_obj.ftype, test_obj.function_name, test_obj.function, arg_list,
                                           func_var)
        func_statement.generate_statement()
        self.statement_description.append(func_statement)
        self.statement_list.append(func_statement.statement)

    def make_constructor(self, test_obj, variable_name=None):
        arg_list = []
        for _, value in test_obj.ktype[1].items():
            statement = self.find_statement(value)
            if statement is not None:
                var_name = statement.statement_variable

            elif self.is_primitive(value):
                var_name = self.generate_variable_name()
                statement = PrimitiveStatement(value, var_name)
                statement.generate_statement()
                self.statement_description.append(statement)
                self.statement_list.append(statement.statement)
            else:
                var_name = self.generate_variable_name()
                constr = list(self.generators[value])[0]
                # print("Constr: ", constr)
                self.make_constructor(constr, var_name)
                # print("Statement: ", self.statement_list[-1])

            arg_list.append(var_name)

        if variable_name is None:
            object_var = self.generate_variable_name()
        else:
            object_var = variable_name

        constr_statement = ConstructorStatement(
            test_obj.ktype, test_obj.klass_name, test_obj.klass, arg_list, object_var)

        constr_statement.generate_statement()
        self.statement_description.append(constr_statement)
        self.statement_list.append(constr_statement.statement)

    def generate_variable_name(self):
        variable = "v" + str(self.count)
        self.count += 1
        return variable

    def find_statement(self, value):
        # checks whether given statement type exists in current statement descriptions and returns items it
        statement_type = ''
        if self.is_primitive(value):
            statement_type = "PrimitiveStatement"
        else:
            statement_type = "ConstructorStatement"

        statement_list = [None]
        for i in range(len(self.statement_description) - 1, -1, -1):
            statement = self.statement_description[i]
            if type(statement).__name__ == statement_type:
                if statement_type == "PrimitiveStatement" and statement.statement_type == value or \
                        statement_type == "ConstructorStatement" and statement.klass == value:
                    statement_list.append(statement)
        s = random.choice(statement_list)
        return s

    def find_coverage(self, output_folder_path='.'):
        file_name = "test_coverage.py"
        folder_path = str(os.path.join(output_folder_path,
                          ("coverage_files_" + self.module_name)))
        globallock.acquire()
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        path = os.path.join(folder_path, file_name)

        if os.path.isfile(path):
            os.remove(path)

        f = open(path, "w+")
        f.write("import coverage\n")

        # uncomment if timeout available
        f.write("import signal\n")
        f.write("def handler(signum, frame):\n")
        f.write("\tprint('Timeout of the test case')\n")
        f.write("\traise Exception('end of time')\n")

        f.write("signal.signal(signal.SIGALRM, handler)\n")
        f.write(f"signal.alarm({self.timeout_time})\n")

        f.write("cov = coverage.Coverage() \n")
        f.write("cov.set_option('run:branch', True) \n")
        f.write("cov.start()\n")
        f.write('try:\n')

        for line in self.statement_list:
            f.write("\t"+line + "\n")

        f.write('except:\n')
        f.write('\twith open("crashed.txt", "w+") as cr_file:\n')
        f.write('\t\tcr_file.write("yes")\n')

        f.write("cov.stop()\n")
        f.write(f"cov.save()\n")
        f.write("cov.json_report()\n")
        f.close()

        # print("in exec exec")
        run_time_error = False
        try:

            exec(open(path).read())
        except Exception as e:
            run_time_error = True
            print("Testcase run failed")
            print(e)

        if os.path.isfile('crashed.txt'):
            run_time_error = True
            print("Testcase run failed")
            os.remove('crashed.txt')

        data = None
        module_path = os.path.join(
            'examples', (utils.relative_path_from_module_name(self.module_name) + ".py"))
        if os.path.isfile('coverage.json'):
            with open('coverage.json', 'r') as report:
                data = json.load(report)

            os.remove(path)
            # print(data)

            # print("Percent covered",
            #       data['files'][module_path]['summary']['percent_covered'])

            os.remove('coverage.json')

        globallock.release()

        if data is None or module_path not in data['files']:
            return None, False

        return data['files'][module_path], run_time_error

    def is_primitive(self, var_type):
        return var_type == int or var_type == bool or var_type == float or var_type == str
