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


def function_in_module(module):
    return lambda member: isfunction(member) and member.__module__ == module.__name__


if __name__ == "__main__":
    sys.path.append(str(Path().parent.absolute()))
    test_module = importlib.import_module("examples.example")
    classes_in_module = getmembers(test_module, class_in_module(test_module))
    functions_in_module = getmembers(test_module, function_in_module(test_module))
    one_function = functions_in_module[0][1]
    t = infer_type(one_function)



