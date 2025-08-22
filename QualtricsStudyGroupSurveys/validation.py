from enum import Enum
from typing import Dict, Any

class Validation_Type(Enum):
    VALIDNUMBER = "ValidNumber"
    MINCHAR     = "MinChar"
    MINCHOICES  = "MinChoices"


class Validation:
    def __init__(self, force_response:bool, type:Validation_Type = None, settings:Dict[str, Any] = None):
        self._force_response = force_response
        self._type = type
        self._settings = settings
    
    def generate_json(self):
        return {
            "validation": {
                "doesForceResponse": self._force_response,
                "type": (self._type.value if self._type is not None else None),
                "settings": self._settings
            }
        }