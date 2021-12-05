from __future__ import annotations
from abc import ABC, abstractmethod
import random
import string
import parse
import os
from pathlib import Path
from statement import *
# from examples.queue_example import Queue



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

    def __init__(self, module_name: str, objects_under_test, limit ):
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
        self.statement_description.append( import_statement )
        self.statement_list.append( import_statement.statement )

        #Retrieve objects_under_test randomly and make corresponding statements
        while ( len( self.objects_under_test) > 0 and  len( self.statement_list ) < self.limit ):
            test_obj = random.choice(list(self.objects_under_test) )
            test_obj_type = type( test_obj).__name__

            if  test_obj_type == "Function" :
                arg_list = []
                for _, value in test_obj.ftype[1].items():
                    var_name = self.generate_variable_name()
                    statement = PrimitiveStatement(value, var_name)
                    statement.generate_statement()

                    self.statement_description.append(statement)
                    self.statement_list.append( statement.statement )
                    arg_list.append( var_name )
            
                func_var = self.generate_variable_name()
                print( func_var )
                func_statement =  FunctionStatement(test_obj.ftype, test_obj.function_name , test_obj.function, arg_list, func_var)
                func_statement.generate_statement()
                self.statement_description.append( func_statement)
                self.statement_list.append( func_statement.statement )

            
            

    def generate_variable_name(self):
        variable = "v" + str(self.count)
        self.count += 1
        return variable
       

    def write_in_file (self):
        file_name = "testcase.py"
        folder_path = str(Path().absolute()) + '/examples'
        path = os.path.join(folder_path,file_name)
        f = open( path, "w")
        for i in self.statement_list:
            f.write(i + "\n")
        f.close()


        



    

           
        
def triangle(x: int, y: int, z: int) -> str:
    if x == y == z:
        return "Equilateral triangle"
    elif x == y or y == z or x == z:
        return "Isosceles triangle"
    else:
        return "Scalene triangle"



# k = parse.infer_type(examples.e)
# j = Queue(20)

# print(k)
triangle.ftype = [[5,6,3], {"x":str, "y": int, "z":int}, [34,45,235]]
triangle.function_name = "traingle"
triangle.function = triangle
a = FunctionTestcase(triangle, "array")
b = a.generate_random_testcase()
print(b)
# a.write_in_file()