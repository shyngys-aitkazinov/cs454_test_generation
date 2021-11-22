from __future__ import annotations
import datetime
import enum
import importlib
import logging
import os
import sys
import threading
from inspect import isfunction, isclass, getmembers, getmodule
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Tuple

class Function(object):
    """
    class representing simple functions
    """

    def __init__(self, function_name, function, ftype=None):
        self.function_name = function_name
        self.function = function
        self.ftype = ftype

    def generator(self):
        pass

class Method (object):
    def __init__(self, method_name, method, mtype = None):
        self.method_name = method_name
        self.method = method
        self.mtype = mtype


class Constructor(object):
    def __init__(self, klass, ctype = None):
        self.klass = klass
        self.ctype = ctype

    def get_type(self):
        return self.ctype


def infer_type(function):
    """

    :param function: generic function
    :return: closure of input arguments and return type
    """

    def resolve_recursively(input_type):
        if type(input_type).__name__ == 'type':
            return input_type.__name__
        elif type(input_type).__name__ == 'tuple':
            r = []
            for x in list(input_type):
                t = resolve_recursively(x)
                r.append(t)
            return tuple(r)
        else:
            raise NotImplementedError

    input_args = []
    for k,v in function.__annotations__.items():
        true_type = resolve_recursively(v)
        if k != 'return':
            input_args.append((k, true_type))
    ret_type = function.__annotations__.setdefault('return').__name__

    return input_args, ret_type




def read_module(path_to_module, module_name):
    pass


class Foo():
    pass


def add(a: Foo, b: Foo) -> Foo:
    return a + b


def class_in_module(module):
    return lambda member: isclass(member) and member.__module__ == module.__name__

def function_in_module ( module: str ):
    return lambda member: isfunction( member ) and member.__module__ == module.__name__
    
def is_protected ( function_name ):
    return function_name.startswith('_')

def add_dependency(klass, analyzed_classes):
    if klass in analyzed_classes:
        print("Analyzed class")
        return analyzed_classes
    analyzed_classes.append(klass)
    construct = Constructor(klass, infer_type(klass.__init__))
    #add dependency
    for method_name, method in getmembers(klass, isfunction):
        method = Method(method_name, method, infer_type(method))
        
    return analyzed_classes

    
        
if __name__ == "__main__":
    sys.path.append(str(Path().parent.absolute()))
    sys.path.append(str(Path().parent.absolute()) + "\\examples")
    test_module = importlib.import_module("examples.example")
    classes_in_module = getmembers(test_module, class_in_module(test_module))
    functions_in_module = getmembers(test_module, function_in_module(test_module))
    one_function = functions_in_module[0][1]
    analyzed_classes = list()
    t = infer_type(one_function)
    for function_name, func in functions_in_module:
        if is_protected(function_name):
            continue

    for _, klass in classes_in_module:
        analyzed_classes = add_dependency(klass, analyzed_classes)



