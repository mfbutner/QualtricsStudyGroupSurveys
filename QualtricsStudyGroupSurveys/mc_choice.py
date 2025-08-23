from typing import Any
from .display_logic import Display_Logic

class Choice:
    def __init__(self, name:str, description:str, display_logic:Display_Logic):
        self._name = name
        self._description = description
        self._display_logic = display_logic
    
    def generate_json(self, index:int) -> dict[str, Any]:
        return {
            "recode":str(index),
            "description":self._name,
            "choiceText":self._description,
            "imageDescription":None,
            "variableName":None,
            "analyze":True
        }