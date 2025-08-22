from enum import Enum
from abc import ABC, abstractmethod

class QuestionType(Enum):
    MC =      0
    DB =      1
    MATRIX =  2
    TE =      3
    SLIDER =  4
    RO =      5
    SBS =     6
    CS =      7
    PGR =     8
    HOTSPOT = 9
    HEATMAP = 10
    DD =      11
    HL =      12
    DRAW =    13
    TIMING =  14
    META =    15
    CAPTCHA = 16


class Question(ABC):
    @abstractmethod
    def __init__(self):
        self._type = None

class Multiple_Choice(Question):
    def __init__(self):
        self._type = QuestionType.MC

class Descriptive_Text(Question):
    def __init__(self):
        self._type = QuestionType.DB

class Text_Or_Grapic(Question):
    def __init__(self):
        self._type = QuestionType.DB
    
class Matrix_Table(Question):
    def __init__(self):
        self._type = QuestionType.MATRIX

class Text_Entry(Question):
    def __init__(self):
        self._type = QuestionType.TE
    
class Slider(Question):
    def __init__(self):
        self._type = QuestionType.SLIDER

class Rank_Order(Question):
    def __init__(self):
        self._type = QuestionType.RO

class Side_By_Side(Question):
    def __init__(self):
        self._type = QuestionType.SBS

class Constant_Sum(Question):
    def __init__(self):
        self._type = QuestionType.CS

class Pick_Group_And_Rank(Question):
    def __init__(self):
        self._type = QuestionType.PGR

class Hot_Spot(Question):
    def __init__(self):
        self._type = QuestionType.HOTSPOT

class Heat_Map(Question):
    def __init__(self):
        self._type = QuestionType.HEATMAP

class Drill_Down(Question):
    def __init__(self):
        self._type = QuestionType.DD

class Net_Promoter_Score(Question):
    def __init__(self):
        self._type = QuestionType.MC

class Highlight(Question):
    def __init__(self):
        self._type = QuestionType.HL

class Signature(Question):
    def __init__(self):
        self._type = QuestionType.DRAW

class Timer(Question):
    def __init__(self):
        self._type = QuestionType.TIMING

class Meta_Info(Question):
    def __init__(self):
        self._type = QuestionType.META

class Captcha(Question):
    def __init__(self):
        self._type = QuestionType.CAPTCHA
