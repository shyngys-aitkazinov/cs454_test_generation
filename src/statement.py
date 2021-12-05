from __future__ import annotations
from abc import ABC, abstractmethod
import testcase
import random
import string


class StatementType:
    StatementTypes = []
    """
    create a statement type class for the statement class
    """

    @classmethod
    def initialize_statement_types(cls, *args, **kwargs):
        pass

    @classmethod
    def get_statement_type(cls, input_statement):
        pass

    """ return the statement type according to the input statement
    """


class AbstractStatement(ABC):

    def __init__(self, statement_type,
                 statement_value,
                 arg_list=None):
        self.statement_type = statement_type
        self.statement_value = statement_value
        self.arg_list = arg_list
        # TODO: might need more attributes


class ImportStatement(AbstractStatement):
    def __init__(self, module):
        self.module = module
        self.statement = ""

    def generate_statement(self):
        self.statement = "from " + self.module + " import *"


class PrimitiveStatement(AbstractStatement):
    def __init__(self, statement_type, statement_variable):
        self.statement_type = statement_type
        self.statement_variable = statement_variable
        self.statement = ""
        self.statement_value = None

    def generate_random_value(self):
        switch = {
            int: random.randint(-1000, 1000),
            bool: bool(random.getrandbits(1)),
            float: random.random(),
            str: ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        }
        self.statement_value = switch.get(self.statement_type)

    def generate_statement(self):
        if (self.statement_value is None):
            self.generate_random_value()

        self.statement = self.statement_variable + " = " + str(self.statement_value)


class FunctionStatement(AbstractStatement):
    def __init__(self, statement_type, function_name, func, arg_list, statement_variable=None):
        self.statement_type = statement_type
        self.function_name = function_name
        self.statement_variable = statement_variable
        self.func = func
        self.arg_list = arg_list
        self.statement = ""

    def generate_statement(self):
        statement = ""
        if self.statement_variable is not None:
            statement += (self.statement_variable + " = ")
        statement += self.function_name + "( " + ', '.join(self.arg_list) + " )"
        self.statement = statement


class ConstructorStatement(AbstractStatement):
    def __init__(self, statement_type, class_name, klass, arg_list, variable ):
        self.statement = ""
        self.statement_variable = variable
        self.arg_list = arg_list
        self.class_name = class_name
        self.klass = klass
        self.statement_type = statement_type
    

    def generate_statement(self):
        statement = self.statement_variable + " = " 
        statement += self.class_name + "(" + ', '.join(self.arg_list) +  " )"
        self.statement = statement
    


class MethodStatement(AbstractStatement):
    def __init__(self, statement_type, method_name, method, obj , arg_list, variable=None):
        self.statement_type = statement_type
        self.method = method
        self.method_name = method_name
        self.arg_list = arg_list
        self.statement_variable = variable
        self.obj = obj
        self.statement = ""


    def generate_statement(self):
        statement = ""
        if self.statement_variable is not None:
            statement += (self.statement_variable + " = ")
        statement += self.obj + '.' + self.method_name + "( " + ', '.join(self.arg_list) + " )"
        self.statement = statement




