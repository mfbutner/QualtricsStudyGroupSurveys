# from enum import Enum
# from typing import Dict, Any

# class Validation_Type(Enum):
#     VALIDNUMBER = "ValidNumber"
#     MINCHAR     = "MinChar"
#     MINCHOICES  = "MinChoices"


# class Validation:
#     def __init__(self, force_response:bool, force_response_type:bool, type:Validation_Type = None, settings:Dict[str, Any] = None):
#         self._force_response = force_response
#         self._force_response_type = force_response_type
#         self._type = type
#         self._settings = settings
    
#     def generate_json(self):
#         output = {"Settings": {
#             "ForceResponse": "ON" if self._force_response else "OFF",
#         }}
#         if self._force_response:
#             output["Settings"]["ForceResponseType"] = "ON" if self._force_response_type else "OFF"
#         output["Settings"]["Type"] = self._type.value if self._type is not None else "None"
#         if (self._settings is not None):
#             for setting in self._settings.keys():
#                 output["Settings"][setting] = self._settings[setting]
        
#         return output

from abc import ABC, abstractmethod
from typing import Dict, Any

# class Validation_Type(Enum):
#     OPTIONAL = 0
#     REQUIRED = 1
#     VALID    = 2

class Validation(ABC):
    @abstractmethod
    def generate_json(self) -> Dict[str, Any]:
        pass


class Optional_Response(Validation):
    def generate_json(self) -> Dict[str, Any]:
        return {
            "Settings": {
                "ForceResponse": "OFF",
                "Type": "None"
            }
        }


class Required_MAVR(Validation):
    def generate_json(self) -> Dict[str, Any]:
        return {
            "Settings": {
                "ForceResponse": "ON",
                "ForceResponseType": "ON",
                "Type": "MinChoices",
                "MinChoices": "1"
            }
        }

class Required_SAVR_DL(Validation):
    def generate_json(self) -> Dict[str, Any]:
        return {
            "Settings": {
                "ForceResponse": "ON",
                "ForceResponseType": "ON",
                "Type": "None"
            }
        }


class Min_Chars(Validation):
    def __init__(self, num_chars:int):
        self._num_chars = num_chars

    def generate_json(self) -> Dict[str, Any]:
        return {
            "Settings": {
                "ForceResponse": "ON",
                "ForceResponseType": "ON",
                "Type": "MinChars",
                "MinChars": f"{self._num_chars}"
            }
        }


class Number_In_Range(Validation):
    def __init__(self, min:int, max:int):
        self._min = min
        self._max = max

    def generate_json(self) -> Dict[str, Any]:
        return {
            "Settings": {
                "ForceResponse": "ON",
                "ForceResponseType": "ON",
                "Type": "ContentType",
                "MinChars": "1",
                "ContentType": "ValidNumber",
                "ValidDateType": "DateWithFormat",
                "ValidPhoneType": "ValidUSPhone",
                "ValidZipType": "ValidUSZip",
                "ValidNumber": {
                    "Min": f"{self._min}",
                    "Max": f"{self._max}",
                    "NumDecimals": "0"
                }
            }
        }