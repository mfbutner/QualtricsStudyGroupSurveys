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