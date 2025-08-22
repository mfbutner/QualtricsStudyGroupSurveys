from enum import Enum
from typing import Dict

class Validation_Type(Enum):
    VALIDNUMBER = 0
    MINCHAR     = 1
    MINCHOICES  = 2


class Validation:
    def __init__(self, force_response:bool, type:Validation_Type = None, settings:Dict[str, int] = None):
        self._force_response = force_response
        self._type = type
        self._settings = settings