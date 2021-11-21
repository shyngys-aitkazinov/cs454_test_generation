from __future__ import annotations
import datetime
import enum
import importlib
import logging
import os
import sys
import threading
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Tuple


def read_module(path_to_module, module_name):
    pass

class Foo():
    pass

def add(a: Foo, b: Foo) -> Foo:
    return a + b

if __name__ == "__main__":

    module = importlib.import_module("examples.example", str(Path().parent.absolute().parent))
    print(add("s", "s"))



