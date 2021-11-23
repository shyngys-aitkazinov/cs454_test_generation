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
import utils


class Function(object):
    """
    class representing simple functions
    """
    def __init__(self, function_name, function, ftype=None):
        self.function_name = function_name
        self.function = function
        self.ftype = ftype


class Method(object):
    def __init__(self, method_name, klass, method, mtype=None):
        self.method_name = method_name
        self.klass = klass
        self.method = method
        self.mtype = mtype


class Constructor(object):
    def __init__(self, klass, klass_name, ktype=None):
        self.klass = klass
        self.klass_name = klass_name
        self.ktype = ktype


def infer_type(function):
    """

    :param function:
    :return: the type information of the callable
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


def class_in_module(module):
    return lambda member: isclass(member) and member.__module__ == module.__name__


def function_in_module(module: str):
    return lambda member: isfunction(member) and member.__module__ == module.__name__


def is_protected(function_name):
    return function_name.startswith('_') and not function_name.startswith('__')


def is_constructor(method_name: str) -> bool:
    return method_name == "__init__"


def method_defined_in_class(method, klass):
    return klass == utils.get_class_that_defined_method(method)


# def add_class(klass, klass_name, recursion_level, analyzed_classes):
#
#     assert(inspect.isclass(klass))
#     methods = []
#     if klass in analyzed_classes:
#         return
#     if hasattr(klass, "__init__"):
#         constructor = Constructor(klass, klass_name, infer_type(klass.__init__))
#     else:
#         constructor = Constructor(klass, klass_name, (None, {}, None))
#
#     for method_name, method in inspect.getmembers(klass, inspect.isfunction):
#
#         m = Method(method_name, klass, method, infer_type(method))
#
#         if is_constructor(method_name) or is_protected(method_name) or \
#                 not method_defined_in_class(method, klass):
#             continue
#         methods.append(m)


class TestCluster:
    """
    Cluster that collects and organizes methods, functions, classes for
    further generation
    """
    def __init__(self):
        self.generators = dict()
        self.modifiers = dict()
        self.objects_under_test = set()
        self.analyzed_classes = set()

    def generate_cluster(self, module_name, pkg=None):
        module = importlib.import_module(module_name, pkg)
        classes_in_module = getmembers(module, class_in_module(module))
        functions_in_module = getmembers(module, function_in_module(module))
        for function_name, func in functions_in_module:
            if is_protected(function_name):
                continue
            fun = Function(function_name, func, infer_type(func))
            self.add_function(fun, True)

        for klass_name, klass in classes_in_module:
            self.add_class(klass, klass_name, 1, True)

    def add_class(self, klass, klass_name, recursion_level, include):

        assert (inspect.isclass(klass))
        # methods = []
        if klass in self.analyzed_classes:
            return
        if hasattr(klass, "__init__"):
            constructor = Constructor(klass, klass_name, infer_type(klass.__init__))
        else:
            constructor = Constructor(klass, klass_name, (None, {}, None))

        self.add_constructor(constructor, include)

        for method_name, method in inspect.getmembers(klass, inspect.isfunction):

            temp_method = Method(method_name, klass, method, infer_type(method))

            if is_constructor(method_name) or is_protected(method_name) or \
                    not method_defined_in_class(method, klass):
                continue
            self.add_method(temp_method, include)

    def add_function(self, function: Function, include):
        ret_type = function.ftype[2]

        if include:
            self.objects_under_test.add(function)

        if ret_type is None or ret_type is type(None) or ret_type in utils.PRIMITIVES:
            return

        if not (ret_type in self.generators):
            self.generators[ret_type] = set()
        self.generators[ret_type].add(function)

    def add_method(self, method, include):
        ret_type = method.mtype[2]

        if include:
            self.objects_under_test.add(method)

        if not(method.klass in self.modifiers):
            self.modifiers[method.klass] = set()
        self.modifiers[method.klass].add(method)

        if ret_type is None or ret_type is type(None) or ret_type in utils.PRIMITIVES:
            return

        if not (ret_type in self.generators):
            self.generators[ret_type] = set()
        self.generators[ret_type].add(method)

    def add_constructor(self, constructor, include):
        ret_type = constructor.klass

        if include:
            self.objects_under_test.add(constructor)

        if ret_type is None or ret_type is type(None) or ret_type in utils.PRIMITIVES:
            return

        if not (ret_type in self.generators):
            self.generators[ret_type] = set()
        self.generators[ret_type].add(constructor)

        # TODO: resolve dependencies


if __name__ == "__main__":
    sys.path.append(str(Path().parent.absolute()))
    sys.path.append(str(Path().parent.absolute()) + "\\examples")
    t = TestCluster()
    t.generate_cluster("examples.example")
    # test_module = importlib.import_module("examples.example")
    # classes_in_module = getmembers(test_module, class_in_module(test_module))
    # functions_in_module = getmembers(test_module, function_in_module(test_module))
    # one_function = functions_in_module[0][1]
    # analyzed_classes = list()
    # t = infer_type(one_function)
    # for function_name, func in functions_in_module:
    #     if is_protected(function_name):
    #         continue
    #     f = Function(function_name, func, infer_type(func))
    #     # add function to cluster
    # for _, klass in inspect.getmembers(module, class_in_module(self._module_name)):
    #     self._add_dependency(klass, 1, True)
    #
    # for _, klass in classes_in_module:
    #     analyzed_classes = add_dependency(klass, analyzed_classes)



