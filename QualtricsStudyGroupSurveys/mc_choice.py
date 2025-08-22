from typing import Any

class Choice:
    def __init__(self, name:str, description:str):
        self._name = name
        self._description = description
    
    def generate_json(self, index:int) -> dict[str, Any]:
        return {
            "recode":index,
            "description":self._name,
            "choiceText":self._description,
            "imageDescription":None,
            "variableName":None,
            "analyze":True
        }