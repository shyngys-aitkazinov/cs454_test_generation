from typing import Optional
import inspect
import types
import os
PRIMITIVES = [int, str, bytes, bool, float, complex]
COLLECTIONS = [list, set, tuple, dict]


def get_class_that_defined_method(method: object) -> Optional[object]:
    """Retrieves the class that defines a method.

    Taken from https://stackoverflow.com/a/25959545/4293396

    Args:
        method: The method

    Returns:
        The class that defines the method
    """
    if inspect.ismethod(method):
        assert isinstance(method, types.MethodType)
        for cls in inspect.getmro(method.__self__.__class__):
            if cls.__dict__.get(method.__name__) is method:
                return cls
        method = method.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(method):
        assert isinstance(method, types.FunctionType)
        module = inspect.getmodule(method)
        attribute_name = method.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0]
        if not hasattr(module, attribute_name):
            return None
        cls = getattr(module, attribute_name)
        if isinstance(cls, type):
            return cls
    return getattr(method, "__objclass__", None)


def relative_path_from_module_name(module_name):
    """

    :param module_name: module_name written with dots e.g. arithmetics.complex
    :return: path
    """

    splitted_version = module_name.strip().split('.')
    return str(os.path.join(*splitted_version))

