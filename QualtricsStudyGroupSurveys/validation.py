from enum import Enum
from typing import Dict

class Validation_Type(Enum):
    VALIDNUMBER = "ValidNumber"
    MINCHAR     = "MinChar"
    MINCHOICES  = "MinChoices"


class Validation:
    def __init__(self, force_response:bool, type:Validation_Type = None, settings:Dict[str, str] = None):
        self._force_response = force_response
        self._type = type
        self._settings = settings
    
    def generate_json(self):
        return {
            "validation": {
                "doesForceResponse": ("true" if self._force_response else "false"),
                "type": (self._type.value if self._type is not None else "null"),
                "settings": (self._settings if self._settings is not None else "null"),
            }
        }
        # output = {"validation": {"doesForceResponse":"true"}} if self._force_response else {"validation": {"doesForceResponse":"false"}}
        # output = {"validation":"true"} if self._force_response else {"validation":"false"}
        # output = "\"validation\": { \"doesForceResponse\": "
        # if not self._force_response:
        #     output["validation"] = {"doesForceResponse":"false"}
        # else:
        #     output["validation"] = {"doesForceResponse":"true"}
        # if self._type is not None:
        #     output["validation"]["type"] = self._type.value
        # if self._settings is not None:
        #     output["validation"]["settings"] = self._settings
        # return output
