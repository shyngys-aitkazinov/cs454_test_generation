from __future__ import annotations
# import datetime
# import enum
from parse import *
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
import ga
import testsuite
from optparse import OptionParser
import utils


def append_all_directories(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        sys.path.append(dirpath)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-e", dest="epochs", action="store",
                      help="number of epochs for ga", type="int", default=10)
    parser.add_option("-p", action="store", dest="population_size", type="int",
                      default=5, help="size of population")
    parser.add_option("-s", "--selection",
                      action="store", type="string", dest="selection_type", default="tournament",
                      help="selection type: Tournament, Roulette Wheel")
    parser.add_option("-m", "--mutation_rate", action="store", type="float", dest="mutation_rate",
                      help="set mutation rate", default=0.5)
    parser.add_option("-t", "--target_module", action="store", type="string", dest="module_name",
                      help="set target module to test using . to specify the relative path, e.g arithmetics.complex",
                      default="obj_example")
    parser.add_option("-c", "--crossover_rate", action="store", type="float", dest="crossover_rate",
                      help="set crossover rate", default=0.5)

    (options, args) = parser.parse_args(sys.argv[1:])

    # append examples folder
    sys.path.append(str(Path().parent.absolute()))
    append_all_directories(str(Path().parent.absolute() / "examples"))
    # sys.path.append(str(Path().parent.absolute() / "examples"))

    # sys.path.append(str(Path().parent.absolute() / "examples" / "arithmetics"))
    # os.listdir(str(Path().parent.absolute() / "examples")

    append_all_directories(str(Path().parent.absolute() / "examples"))

    # output path
    output_folder_path = str(Path().parent.absolute() / "outputs")

    cluster = TestCluster()

    module_name = options.module_name
    print(module_name)

    cluster.generate_cluster("examples." + module_name)

    ga_config = {
        "pop_size": options.population_size,
        "mutation_rate": options.mutation_rate,
        "crossover_rate": options.crossover_rate,
        "module_name": (module_name, utils.relative_path_from_module_name(module_name)),
        "limit_test_lines": 10,
        "limit_suite_testcases": 4,
        "sut_info": cluster,
        "output_folder_path": output_folder_path,
        "selection": options.selection_type
    }

    Ga = ga.GA(ga_config)
    Ga.run_ga(options.epochs)
