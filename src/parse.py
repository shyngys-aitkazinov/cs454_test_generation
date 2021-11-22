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


def read_module(path_to_module, module_name):
    pass

class Foo():
    pass

def add(a: Foo, b: Foo) -> Foo:
    return a + b

def class_in_module ( module: str):
    return lambda member: isclass(member) and member.__module__ == module.__name__

def function_in_module ( module: str ):
    return lambda member: isfunction( member ) and member.__module__ == module.__name__
    
if __name__ == "__main__":
    sys.path.append(str(Path().parent.absolute()))
    module = importlib.import_module("examples.example")
    classes_in_module = getmembers( module, class_in_module( module ) )
    functions_in_module =  getmembers( module, function_in_module( module ) )




