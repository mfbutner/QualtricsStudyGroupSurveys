from enum import Enum
from typing import Any, List

class Operator(Enum): # can add more if needed
    EQUAL_TO = 0
    NOT_EQUAL_TO = 1

class Logic_Type(Enum):
    EMBEDDED_FIELD = 0
    PANEL_DATA = 1
    QUESTION = 2

class Joining_Type(Enum):
    EXPRESSION = "Expression"
    BOOLEAN_EXPRESSION = "BooleanExpression"
    IF = "If"
    AND_IF = "AndIf"
    OR_DIF = "OrIf"

class Conjunction(Enum):
    AND = 0
    OR = 1
    NONE = 2

class Sub_Display_Logic:
    def __init__(self, logic_type:Logic_Type, lhs:str, operator:Operator, rhs:str, type:Joining_Type, description:str, conjunction:Conjunction = None):
        self._logic_type = logic_type
        self._lhs = lhs
        self._operator = operator
        self._rhs = rhs
        self._type = type
        self._description = description
        self._conjunction = conjunction

class Display_Logic:
   def __init__(self, sub_logics:dict[List[Sub_Display_Logic], Joining_Type], type:Joining_Type):
       self._sub_logics = sub_logics
       self._type = type