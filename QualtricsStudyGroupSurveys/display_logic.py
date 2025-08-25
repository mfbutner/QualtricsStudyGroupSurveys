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
    
    def generate_json(self) -> dict[str, Any]:
        output = {
            "LogicType": self._logic_type,
            "LeftOperand": self._lhs,
            "Operator": self._operator,
            "RightOperand": self._rhs,
            "Type":self._type,
            "Description": self._description,
        }
        if self._conjunction is not None:
            output["Conjunction"] = self._conjunction
        return output

class Display_Logic:
    def __init__(self, sub_logics:List[Sub_Display_Logic], type:Joining_Type):
       self._sub_logics = sub_logics
       self._type = type
    
    def generate_json(self) -> dict[str, Any]:
        output = {
            f"{i}": sub_logic.generate_json() for (i,sub_logic) in enumerate(self._sub_logics)
        }
        output["Type"] = self._type.value
        return output           

class Display_Logic_Field:
    def __init__(self, display_logic:List[Display_Logic], joining_type:Joining_Type=None):
        self._display_logic = display_logic
        self._joining_type = joining_type
    
    def generate_json(self):
        output = {}
        for (i, display_logic) in enumerate(self._display_logics):
            output[f"{i}"] = display_logic.generate_json()
        if self._joining_type is not None:
            output["Type"] = self._joining_type
        output["inPage"] = False
        return output