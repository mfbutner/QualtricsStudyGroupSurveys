from abc import ABC, abstractmethod
from typing import List, Any
from .mc_choice import Choice
from .validation import Validation
from enum import Enum

class Selector(Enum):
    SL = 0
    ESTB = 1
    DL = 2
    MAVR = 3
    SAVR = 4

class Question(ABC):
    def __init__(self, name:str, description:str, validation:Validation):
        self._name = name
        self._description = description
        self._validation = validation
    
    @abstractmethod
    def generate_json(self) -> dict[str, Any]:
        pass

class Multiple_Choice(Question):
    def __init__(self, name:str, description:str, validation:Validation, selector:Selector, usesSubSelector:bool, choices:List[Choice] = None):
        super().__init__(name, description, validation)
        self._selector = selector
        self._usesSubSelector = usesSubSelector
        self._choices = choices if choices is not None else []
    
    def addChoice(self, choice:Choice):
        self._choices.append(choice)
    
    def generate_json(self) -> dict[str, Any]:
        return {
            "questionType": {
                "type":"MC",
                "selector":self._selector.name,
                "subSelector":"TX" if self._usesSubSelector else None,
            },
            "questionText":self._description,
            "questionLabel":None,
            "validation":self._validation.generate_json(),
            "questionName":self._name,
            "choices":{
                str(i + 1): choice.generate_json(i) for (i, choice) in enumerate(self._choices)
            }
        }        

    
class Text_Entry(Question):
    def __init__(self, name:str, description:str, validation:Validation, selector:Selector):
        super().__init__(name, description, validation)
        self._selector = selector
    
    def generate_json(self) -> dict[str, Any]:
        return {
            "questionType": {
                "type":"TE",
                "selector":self._selector.name, 
                "subSelector":None
            },
            "questionText":self._description,
            "questionLabel":None,
            "validation":self._validation.generate_json(),
            "questionName":self._name
        }


class File_Upload(Question):
    def __init__(self, name:str, description:str, validation:Validation):
        super().__init__(name, description, validation)
    
    def generate_json(self) -> dict[str, Any]:
        return {
            "questionType": {
                "type":"FileUpload", 
                "selector":"FileUpload",
                "subSelector":None
            },
            "questionText":self._description,
            "questionLabel":None,
            "validation":self._validation.generate_json(),
            "questionName":self._name
        }



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
