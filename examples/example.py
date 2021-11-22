#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2021 Pynguin Contributors
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#

import queue_example
from queue_example import Queue
from typing import Tuple


def triangle(x: Tuple[int, int, int], y: int, z: int) -> str:
    if x[0] == y == z:
        return "Equilateral triangle"
    elif x[0] == y or y == z or x == z:
        return "Isosceles triangle"
    else:
        return "Scalene triangle"


class A:
    def __init__(self):
        pass

    def f(self, data: str) -> None:
        print(data)