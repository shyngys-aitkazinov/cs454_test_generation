from __future__ import annotations
import datetime
import enum
import importlib
import logging
import os
import sys
import threading
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Tuple, Callable, Any
from inspect import isclass, isfunction, getmembers


def function_in_module(module_name: str) -> Callable[[Any], bool]:
    return lambda member: isfunction(member)


def class_in_module(module_name: str) -> Callable[[Any], bool]:
    return lambda member: isclass(member)

def read_module(path_to_module, module_name):
    pass

# class Foo():
#     pass
#
# def add(a: Foo, b: Foo) -> Foo:
#     return a + b

if __name__ == "__main__":
    print(os.getcwd())
    # print(str(Path().parent.absolute().parent))
    # sys.path.append(str(Path().parent.absolute()))
    module = importlib.import_module("examples.example")
    a = getmembers(module, class_in_module(module))
    b = getmembers(module, function_in_module(module))


    # print(add("s", "s"))




