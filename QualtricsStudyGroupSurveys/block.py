from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .question import Question
class Block():
    def __init__(self, description:str):
        self._description = description
    
    def generate_json(self) -> Dict[str, Any]:
        return {
            "Type": "Standard",
            "SubType": "",
            "Description": self._description,
            "BlockElements": [], # Must be empty to create, according to API
            "Options": {
                "BlockLocking": "false",
                "RandomizeQuestions": "false",
                "BlockVisibility": "Expanded"
            }
        }
