from typing import Any
from .display_logic import Display_Logic_Field

class Choice:
    def __init__(self, name:str, description:str, exclusive_answer:bool=False, display_logic:Display_Logic_Field=None):
        self._name = name
        self._description = description
        self._exclusive_answer = exclusive_answer
        self._display_logic = display_logic
    
    def generate_json(self) -> dict[str, Any]:
        output = {
            "Display": self._name,
        }
        if (self._exclusive_answer):
            output["ExclusiveAnswer"] = True
        if self._display_logic is not None:
            output["DisplayLogic"] = self._display_logic.generate_json()

        return output