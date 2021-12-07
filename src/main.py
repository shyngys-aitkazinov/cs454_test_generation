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







if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-e", dest="epochs", action="store",
                      help="number of epochs for ga", type="int", default=10)
    parser.add_option("-p", action="store", dest="population_size", type="int",
                      default=20, help="size of population")
    parser.add_option("-s", "--selection",
                      action="store", type="string", dest="selection_type", default="tournament",
                      help="selection type: Tournament, Roulette Wheel")
    parser.add_option("-l", "--local_search", action="store_true", dest="local_search",
                      help="to apply local search, add this flag", default=False)
    parser.add_option("-n", "--no_elitism", action="store_false", dest="elitism",
                      help="turn off elitism", default=True)
    parser.add_option("-m", "--mutation_rate", action="store", type="float", dest="mutation_rate",
                      help="set mutation rate", default=0.05)
    parser.add_option("-r", "--read_population", action="store", type="string", dest="load_population",
                      help="start with predefined population: csv file", default=None)

    (options, args) = parser.parse_args(sys.argv[2:])

    # append examples folder
    sys.path.append(str(Path().parent.absolute()))
    sys.path.append(str(Path().parent.absolute() / "examples"))

    # output path
    output_folder_path = str(Path().parent.absolute() / "outputs")


    cluster = TestCluster()
    module_name = sys.argv

    module_name = "obj_example"
    t.generate_cluster("examples." + module_name)

    ga_config= {
                    "pop_size": 10,
                    "mutation_rate": 0.7,
                    "crossover_rate": 0.4,
                    "number_of_testsuits": 10,
                    "module_name": module_name,
                    "limit_test": 10,
                    "limit_suite": 4,
                    "sut_info": t,
                    "path": output_folder_path
                }

    Ga = ga.GA(ga_config)
    Ga.run_ga(4)