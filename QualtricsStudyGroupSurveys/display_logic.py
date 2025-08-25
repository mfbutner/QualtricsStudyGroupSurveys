from abc import ABC, abstractmethod
from typing import Dict, Any
from .student import Student

class Display_Logic(ABC):
    @abstractmethod
    def generate_json(self, choice_number:int) -> Dict[str, Any]:
        pass

class Display_My_Team(Display_Logic):
    def __init__(self, student:Student):
        self._student = student
    
    def generate_json(self, choice_number:int):
        return {
            f"{choice_number}": {
                "0": {
                    "LogicType": "EmbeddedField",
                    "LeftOperand": "Team",
                    "Operator": "EqualTo",
                    "RightOperand": f"{self._student._team}",
                    "Type": "Expression",
                    # "Description": fr"<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Team</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> f{self._team_number} </span>"
                },
                "1": {
                    "LogicType": "PanelData",
                    "LeftOperand": "m://Email1",
                    "Operator": "NotEqualTo",
                    "RightOperand": f"{self._student._email}",
                    "Type": "Expression",
                    # "Description": fr"<span class=\"ConjDesc\">And</span><span class=\"schema_desc\">Contact List</span><span class=\"select_val_desc LeftOperand_desc\">Email</span><span class=\"select_val_desc Operator_desc\">Is Not Equal to</span><span class=\"textbox_val_desc RightOperand_desc\">{self._student._email}</span>",
                    "Conjunction": "And"
                },
                "Type": "If"
            },
            "Type": "BooleanExpression",
            "inPage": False
        }

class Display_Only_If_Response_Matches(Display_Logic):
    def __init__(self, question_ID:str):
        self._question_ID = question_ID

    def generate_json(self, choice_number:int):
        return {
            f"{choice_number}": {
                "0": {
                    "LogicType": "Question",
                    "QuestionID": self._question_ID,
                    "QuestionIsInLoop": "no",
                    "ChoiceLocator": f"q://{self._question_ID}/ChoiceTextEntryValue",
                    "Operator": "EqualTo",
                    "QuestionIDFromLocator": f"{self._question_ID}",
                    "LeftOperand": f"q://{self._question_ID}/ChoiceTextEntryValue",
                    "RightOperand": "0",
                    "Type": "Expression",
                    # "Description": fr"<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Team</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> f{self._team_number} </span>"
                },
                "Type": "If"
            },
            "Type": "BooleanExpression",
            "inPage": False
        }

