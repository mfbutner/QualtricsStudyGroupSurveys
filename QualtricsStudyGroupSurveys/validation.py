from enum import Enum
from typing import Dict, Any

class Validation_Type(Enum):
    VALIDNUMBER = "ValidNumber"
    MINCHAR     = "MinChar"
    MINCHOICES  = "MinChoices"


class Validation:
    def __init__(self, force_response:bool, force_response_type:bool, type:Validation_Type = None, settings:Dict[str, Any] = None):
        self._force_response = force_response
        self._force_response_type = force_response_type
        self._type = type
        self._settings = settings
    
    def generate_json(self):
        output = {"Settings": {
            "ForceResponse": "ON" if self._force_response else "OFF",
        }}
        if self._force_response:
            output["Settings"]["ForceResponseType"] = "ON" if self._force_response_type else "OFF"
        output["Settings"]["Type"] = self._type.value if self._type is not None else "None"
        if (self._settings is not None):
            for setting in self._settings.keys():
                output["Settings"][setting] = self._settings[setting]
        
        return output