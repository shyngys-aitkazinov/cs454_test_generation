from __future__ import annotations
import datetime
import enum
import importlib
import logging
import os
import sys
import threading
from inspect import isfunction, isclass, getmembers, ismethod, getmro
from pathlib import Path
from typing import TYPE_CHECKING, Optional
import typing
import inspect

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

    :param function:
    :return: the type information of the function or method
    """
    signature = inspect.signature(function)
    parameters = {}
    hints = typing.get_type_hints(function)
    for param_name in signature.parameters:
        if param_name == "self":
            continue
        type_hint = hints.get(param_name, None)
        type_hint = wrap_var_param_type(type_hint, signature.parameters[param_name].kind)
        parameters[param_name] = type_hint

    ret_type = hints.get('return', None)

    return signature, parameters, ret_type

def wrap_var_param_type(type_, param_kind):

    if param_kind == inspect.Parameter.VAR_POSITIONAL:
        if type_ is None:
            return typing.List[typing.Any]
        return typing.List[type_]  # type: ignore
    if param_kind == inspect.Parameter.VAR_KEYWORD:
        if type_ is None:
            return typing.Dict[str, typing.Any]
        return typing.Dict[str, type_]  # type: ignore
    return type_


class Foo():
    pass


def add(a: Foo, b: Foo) -> Foo:
    return a + b


def class_in_module(module):
    return lambda member: isclass(member) and member.__module__ == module.__name__


def function_in_module(module: str):
    return lambda member: isfunction( member ) and member.__module__ == module.__name__
    
def is_protected ( function_name ):
    return function_name.startswith('_') and not function_name.startswith('__')


def method_defined_in_class ( klass, method ):
    #get class that defined method
    print( method )
    print( ismethod( method ) )
    if ( ismethod( method)):
        print( getmro(method.__self__.__class__))
        # elif (isfunction( method )):

    # defined_class =
    return True


def is_protected(function_name):
    return function_name.startswith('_')


def add_dependency(klass, analyzed_classes):
    if klass in analyzed_classes:
        print("Analyzed class")
        return analyzed_classes
    analyzed_classes.append(klass)
    # construct = Constructor(klass, infer_type(klass.__init__))
    #add dependency
    for method_name, method in getmembers(klass, isfunction):
        # method = Method(method_name, method, infer_type(method))
        print( method_name)
        method_defined_in_class( klass, method)
        if ( is_constructor( method ) or is_protected( method_name ) or not method_defined_in_class( klass, method)):
            continue
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



