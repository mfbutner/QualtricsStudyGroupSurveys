from abc import ABC, abstractmethod
from typing import List, Any
from .mc_choice import Choice
from .validation import Validation
from .display_logic import Display_Logic
from enum import Enum

class Selector(Enum):
    SL = 0
    ESTB = 1
    DL = 2
    MAVR = 3
    SAVR = 4

class Question(ABC):
    def __init__(self, name:str, block_ID:str, description:str, validation:Validation):
        self._name = name
        self._ID = None
        self._block_ID = block_ID
        self._description = description
        self._validation = validation
        self._display_logic = None
    
    @abstractmethod
    def generate_json(self) -> dict[str, Any]:
        pass

    def get_ID(self) -> str:
        return self._ID if self._ID is not None else "No ID set!"

    def set_ID(self, ID:str):
        self._ID = ID

class Multiple_Choice(Question):
    def __init__(self, name:str, block_ID:str, description:str, validation:Validation, selector:Selector, usesSubSelector:bool, choices:List[Choice]):
        super().__init__(name, block_ID, description, validation)
        self._selector = selector
        self._usesSubSelector = usesSubSelector
        self._choices = choices
    
    def addChoice(self, choice:Choice):
        self._choices.append(choice)
    
    def generate_json(self) -> dict[str, Any]:
        start = {
            "QuestionText":self._description,
            "DefaultChoices":False,
            "DataExportTag":self._name,
            # "QuestionID":self._ID,
            "QuestionType":"MC",
            "Selector":self._selector.name,
        }
        if self._usesSubSelector:
            start["SubSelector"] = "TX"
        end = {
            "DataVisibility": {
                "Private":False,
                "Hidden":False
            },
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            },
            "QuestionDescription":self._description,
            "Choices":{
                str(i + 1): choice.generate_json() for (i, choice) in enumerate(self._choices)
            },
            "ChoiceOrder": [(i+1) for i in range(len(self._choices))],
            "Validation": self._validation.generate_json(),
            "GradingData": [],
            "Language": [],
            "NextChoiceId": 1 + len(self._choices),
            "NextAnswerId": 1,
            "QuestionText_Unsafe": self._description
        }

        return start | end
    
class Text_Entry(Question):
    def __init__(self, name:str, block_ID:str, description:str, validation:Validation, selector:Selector, display_logic:Display_Logic):
        super().__init__(name, block_ID, description, validation)
        self._selector = selector
        self._display_logic = display_logic
    
    def generate_json(self) -> dict[str, Any]:
        output = {
            "QuestionText": self._description,
            "DefaultChoices": False,
            "DataExportTag": self._name,
            # "QuestionID": self._ID,
            "QuestionType": "TE",
            "Selector": self._selector.name,
            "DataVisibility": {
                "Private": False,
                "Hidden": False,
            },
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            },
            "QuestionDescription": self._description,
            "Validation": self._validation.generate_json(),
            "GradingData": [],
            "Language": [],
            "NextChoiceId": 4, # TODO: This shouldn't be hardcoded. How is it generated?
            "NextAnswerId": 1,
            "SearchSource": {
                "AllowFreeResponse": False
            },
            "QuestionText_Unsafe": self._description,
        }
        if self._display_logic is not None:
            output["DisplayLogic"] = self._display_logic.generate_json()
        
        return output



class File_Upload(Question):
    def __init__(self, name:str, block_ID:str, description:str, validation:Validation, display_logic:Display_Logic):
        super().__init__(name, block_ID, description, validation)
        self._display_logic = display_logic
    
    def generate_json(self) -> dict[str, Any]:
        output = {
            "QuestionText": self._description,
            "DefaultChoices": False,
            "DataExportTag": self._name,
            "QuestionType": "FileUpload",
            "Selector": "FileUpload",
            "DataVisibility": {
                "Private": False,
                "Hidden": False,
            },
            "Configuration": {
                "QuestionDescriptionOption": "UseText",
                "MinSeconds": "0",
                "MaxSeconds": "0",
                "AudioOnly": False,
                "VideoUpload": False
            },
            "QuestionDescription": self._description,
            "Validation": self._validation.generate_json(),
            "GradingData": [],
            "Language": [],
            "NextChoiceId": 4, # TODO: This shouldn't be hardcoded. How is it generated?
            "NextAnswerId": 1,
            "ScreenCaptureText": "Capture Screen",
            # "QuestionID": self._ID,
            "QuestionText_Unsafe": self._description,
        }
        if self._display_logic is not None:
            output["DisplayLogic"] = self._display_logic.generate_json()
        
        return output



# These are defined in the docs, but we might not need them:

# class Text_Or_Grapic(Question):
#     def __init__(self):
#         pass
    
# class Matrix_Table(Question):
#     def __init__(self):
#         pass

# class Descriptive_Text(Question):
#     def __init__(self, name:str, description:str, force_response:bool):
#         super().__init__()
    
# class Slider(Question):
#     def __init__(self):
#         pass

# class Rank_Order(Question):
#     def __init__(self):
#         pass

# class Side_By_Side(Question):
#     def __init__(self):
#         pass

# class Constant_Sum(Question):
#     def __init__(self):
#         pass

# class Pick_Group_And_Rank(Question):
#     def __init__(self):
#         pass

# class Hot_Spot(Question):
#     def __init__(self):
#         pass

# class Heat_Map(Question):
#     def __init__(self):
#         pass
# class Drill_Down(Question):
#     def __init__(self):
#         pass

# class Net_Promoter_Score(Question):
#     def __init__(self):
#         pass

# class Highlight(Question):
#     def __init__(self):
#         pass

# class Signature(Question):
#     def __init__(self):
#         pass

# class Timer(Question):
#     def __init__(self):
#         pass

# class Meta_Info(Question):
#     def __init__(self):
#         pass

# class Captcha(Question):
#     def __init__(self):
#         pass
