from __future__ import annotations
import simple

def multiply1(x: int, y: int) -> int:
    my_add = simple.add()

    if y > 0:
        y = y
    else:
        y = -y
        x = -x

    result = 0
    for i in range(y):
        result = my_add(result, x)

    return result


def multiply2(x: int, y: int) -> int:


    return x*y



def substract(x: int, y: int) -> int:

    my_sub = simple.substract()
    return my_sub(x, y)