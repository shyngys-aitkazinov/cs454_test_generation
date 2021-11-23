from __future__ import annotations
from abc import ABC, abstractmethod
import random
import string
import parse
import os
from pathlib import Path

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

class FunctionTestcase(AbstractTestcase):
    def __init__(self, function_info : parse.Function, module_name: str):
        self.function_info = function_info
        self.module_name = module_name
        self.count = 0
        self.statement_list = []
    
    def generate_random_testcase(self):
        ftype = self.function_info.ftype
        function_name = self.function_info.function_name

        args = ftype[0]
        rettype = ftype[1]

        function_args = []

        self.add_module_import()

        for i in args:
            if i[0] not in function_args:
                self.generate_assignment(i)
                function_args.append(i[0])

        statement = self.module_name + "." + function_name + "( " + ', '.join(function_args) +" )"
        if rettype != "None":
            function_var = self.generate_variable_name()
            statement = function_var + " = " + statement
        self.statement_list.append(statement)
        
    def add_module_import(self):
        statement = "import " + self.module_name 
        self.statement_list.append(statement)
        return

    def generate_assignment(self, assignment):
        variable_name = assignment[0]
        variable_type = assignment[1]
        value = self.get_value_for_type(variable_type)
        statement = variable_name + " = " + str(value)
        self.statement_list.append(statement)

    def generate_variable_name( self ):
        variable = "v" + str(self.count)
        self.count += 1
        return variable

    def get_value_for_type ( self, type):
        switch = {
            "int": random.randint( -1000, 1000),
            "boolean": bool(random.getrandbits(1)),
            "float": random.random(),
            "str": ''.join(random.choices(string.ascii_lowercase + string.digits, k = 10))
        }
        return switch.get(type)

    def write_in_file (self):
        file_name = "testcase.py"
        folder_path = str(Path().absolute()) + '\\examples'
        path = os.path.join(folder_path,file_name)
        f = open( path, "w")
        for i in self.statement_list:
            f.write(i + "\n")
        f.close()

    

           
        




    

