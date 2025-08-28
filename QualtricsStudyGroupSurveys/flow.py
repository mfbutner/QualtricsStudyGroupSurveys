from abc import ABC, abstractmethod
from typing import Any, List

# from enum import Enum
# class Embedded_Data_Types(Enum): # Can be added if more flexibility is desired
#     TEAM = 0
#     RECIPIENT_EMAIL = 1


class Flow(ABC):
    def __init__(self, flow_ID:str):
        self._flow_ID = flow_ID
    
    @abstractmethod
    def generate_json(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def length(self) -> int:
        pass

class Root(Flow):
    def __init__(self, flow_ID:str, sub_flows:List[Flow]):
        super().__init__(flow_ID)
        self._sub_flows = sub_flows
    
    def generate_json(self) -> dict[str, Any]:
        count = 1
        for flow in self._sub_flows:
            count += flow.length()
        return {
            "Type": "Root",
            "FlowID": self._flow_ID,
            "Flow": [flow.generate_json() for flow in self._sub_flows],
            "Properties": {
                "Count": count
            }
        }
    
    def length(self):
        return 1


class Embedded_Data(Flow):
    def __init__(self, flow_ID:str):
        super().__init__(flow_ID)
    
    def generate_json(self) -> dict[str, Any]:
        return {
            "Type": "EmbeddedData",
            "FlowID": self._flow_ID,
            "EmbeddedData": [
                {
                    "Description": "Team",
                    "Type": "Recipient",
                    "Field": "Team",
                    "VariableType": "String",
                    "DataVisibility": [],
                    "AnalyzeText": False
                },
                {
                    "Description": "RecipientEmail",
                    "Type": "Recipient",
                    "Field": "RecipientEmail",
                    "VariableType": "String",
                    "DataVisibility": [],
                    "AnalyzeText": False
                }
            ]
        }
    
    def length(self):
        return 1


class Standard(Flow):
    def __init__(self, flow_ID:str, block_ID:str):
        super().__init__(flow_ID)
        self._block_ID = block_ID
    
    def generate_json(self) -> dict[str, Any]:
        return {
            "Type": "Standard",
            "ID": self._block_ID,
            "FlowID": self._flow_ID,
            "Autofill": []
        }
    
    def length(self):
        return 1


class Branch_Logic():
    def __init__(self, question_ID:str):
        self._question_ID = question_ID

    def generate_json(self):
        return {
            "0": {
                "0": {
                    "LogicType": "Question",
                    "QuestionID": self._question_ID,
                    "QuestionIsInLoop": "no",
                    "ChoiceLocator": f"q://{self._question_ID}/ChoiceTextEntryValue",
                    "Operator": "EqualTo",
                    "QuestionIDFromLocator": self._question_ID,
                    "LeftOperand": f"q://{self._question_ID}/ChoiceTextEntryValue",
                    "RightOperand": "0",
                    "IgnoreCase": 1,
                    "Type": "Expression",
                    "Description": "<span class=\"ConjDesc\">If</span> <span class=\"QuestionDesc\">How many times did you meet with your group this week? Report at most your top 10 interactions.</span> <span class=\"LeftOpDesc\">Text Response</span> <span class=\"OpDesc\">Is Equal to</span> <span class=\"RightOpDesc\"> 0 </span>"
                },
                "Type": "If"
            },
            "Type": "BooleanExpression",
        }


class Branch(Flow):
    def __init__(self, flow_ID:str, branch_logic:Branch_Logic, branch_flow:List[Flow]):
        super().__init__(flow_ID)
        self._branch_logic = branch_logic
        self._branch_flow = branch_flow
    
    def generate_json(self) -> dict[str, Any]:
        return {
            "Type": "Branch",
            "FlowID": self._flow_ID,
            "Description": "New Branch",
            "BranchLogic": self._branch_logic.generate_json(),
            "Flow": [flow.generate_json() for flow in self._branch_flow]
        }
    
    def length(self):
        length = 1
        for flow in self._branch_flow:
            length += flow.length()
        return length


class End_Survey(Flow):
    def __init__(self, flow_ID:str):
        super().__init__(flow_ID)
    
    def generate_json(self) -> dict[str, Any]:
        return {
            "Type": "EndSurvey",
            "FlowID": self._flow_ID
        }
    
    def length(self):
        return 1