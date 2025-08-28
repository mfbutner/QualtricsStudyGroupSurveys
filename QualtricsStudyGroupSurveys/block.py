from typing import Dict, Any

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

class Looping_Block(Block):
    def __init__(self, description:str, looping_condition_qid:str):
        super().__init__(description)
        self._looping_condition_qid = looping_condition_qid
    
    def generate_json(self) -> Dict[str, Any]:
        return {
            "Type": "Standard",
            "SubType": "",
            "Description": self._description,
            "BlockElements": [], # Must be empty to create, according to API
            "Options": {
                "BlockLocking": "false",
                "RandomizeQuestions": "false",
                "BlockVisibility": "Expanded",
                "Looping": "Question",
                "LoopingOptions": {
                    "Locator": f"q://{self._looping_condition_qid}/LoopAndMerge/MergeOnNumericResponse?v=10",
                    "QID": self._looping_condition_qid,
                    "ChoiceGroupLocator": f"q://{self._looping_condition_qid}/LoopAndMerge/MergeOnNumericResponse",
                    "Static": {
                    "1": {
                        "2": "1st"
                    },
                    "2": {
                        "2": "2nd"
                    },
                    "3": {
                        "2": "3rd"
                    },
                    "4": {
                        "2": "4th"
                    },
                    "5": {
                        "2": "5th"
                    },
                    "6": {
                        "2": "6th"
                    },
                    "7": {
                        "2": "7th"
                    },
                    "8": {
                        "2": "8th"
                    },
                    "9": {
                        "2": "9th"
                    },
                    "10": {
                        "2": "10th"
                    }
                    },
                    "Randomization": "None"
                }
            }
        }
