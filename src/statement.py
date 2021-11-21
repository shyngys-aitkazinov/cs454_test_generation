from __future__ import annotations
from abc import ABC, abstractmethod


class StatementType:
    StatementTypes = []
    """
    create a statement type class for the statement class
    """

    @classmethod
    def initialize_statement_types(cls, *args, **kwargs):
        pass

    @classmethod
    def get_statement_type(cls, input_statement):
        pass
    """ return the statement type according to the input statement
    """


class AbstractStatement(ABC):

    def __init__(self, statement_type,
                 statement_value,
                 arg_list=None):
        self.statement_type = statement_type
        self.statement_value = statement_value
        self.arg_list = arg_list
        # TODO: might need more attributes


