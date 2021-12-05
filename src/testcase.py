from __future__ import annotations
from abc import ABC, abstractmethod
import random
import string
import parse
import os
from pathlib import Path
from statement import *


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


class Testcase(AbstractTestcase):

    def __init__(self, module_name: str, objects_under_test, limit):
        # self.function_info = function_info
        self.module_name = module_name
        self.count = 0
        self.statement_list = []
        self.statement_description = []
        self.objects_under_test = objects_under_test
        self.limit = limit

    def generate_random_testcase(self):
        # Add import statement
        import_statement = ImportStatement(self.module_name)
        import_statement.generate_statement()
        self.statement_description.append(import_statement)
        self.statement_list.append(import_statement.statement)

        # Retrieve objects_under_test randomly and make corresponding statements
        while (len(self.objects_under_test) > 0 and len(self.statement_list) < self.limit):
            test_obj = random.choice(list(self.objects_under_test))
            test_obj_type = type(test_obj).__name__
        

            if test_obj_type == "Function":
                self.make_function( test_obj )

            elif test_obj_type == "Constructor":
                self.make_constructor( test_obj )

            elif test_obj_type == "Method":
                klass = test_obj.klass
                constructor_obj = parse.Constructor( klass, klass.__name__, parse.infer_type(klass.__init__) )
                obj_name = self.generate_variable_name()
                self.make_constructor( constructor_obj, obj_name ) 
                self.make_method( test_obj, obj_name )

              
             
    def make_method( self, test_obj, obj_name ):
        arg_list = []
        for _, value in test_obj.mtype[1].items():
            var_name = self.generate_variable_name()
            if self.is_primitive( value ):
                statement = PrimitiveStatement(value, var_name)
            statement.generate_statement()

            self.statement_description.append(statement)
            self.statement_list.append(statement.statement)
            arg_list.append(var_name)

        method_var = self.generate_variable_name()
        method_statement = MethodStatement( test_obj.mtype, test_obj.method_name , test_obj.method, obj_name , arg_list, method_var )
        method_statement.generate_statement()
        self.statement_description.append( method_statement)
        self.statement_list.append(method_statement.statement)

    def make_function( self, test_obj ):
        arg_list = []
        for _, value in test_obj.ftype[1].items():
            var_name = self.generate_variable_name()
            if self.is_primitive( value ):
                statement = PrimitiveStatement(value, var_name)
            statement.generate_statement()

            self.statement_description.append(statement)
            self.statement_list.append(statement.statement)
            arg_list.append(var_name)

        func_var = self.generate_variable_name()
        func_statement = FunctionStatement(test_obj.ftype, test_obj.function_name, test_obj.function, arg_list,
                                            func_var)
        func_statement.generate_statement()
        self.statement_description.append(func_statement)
        self.statement_list.append(func_statement.statement)

    def make_constructor(self, test_obj, variable_name = None):
        arg_list = []
        for _, value in test_obj.ktype[1].items():
            var_name = self.generate_variable_name()
            if self.is_primitive( value ):
                print( "Is primitive" )
                statement = PrimitiveStatement( value, var_name )
                
            statement.generate_statement()
            self.statement_description.append(statement)
            self.statement_list.append(statement.statement)
            arg_list.append(var_name)

        if variable_name is None:
            object_var  = self.generate_variable_name()
        else:
            object_var = variable_name

        constr_statement = ConstructorStatement( test_obj.ktype, test_obj.klass_name, test_obj.klass, arg_list, object_var) 
        constr_statement.generate_statement()
        self.statement_description.append(constr_statement)
        self.statement_list.append( constr_statement.statement)    

    def generate_variable_name(self):
        variable = "v" + str(self.count)
        self.count += 1
        return variable

    def write_in_file(self):
        file_name = "testcase.py"
        folder_path = str(Path().absolute()) + '/examples'
        path = os.path.join(folder_path, file_name)
        f = open(path, "w")
        for i in self.statement_list:
            f.write(i + "\n")
        f.close()

    def is_primitive( self, var_type ):
        return var_type == int or var_type == bool or var_type == float or var_type == str










