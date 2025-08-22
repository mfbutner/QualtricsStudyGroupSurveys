from .question import Question
from .qualtrics_connection import QualtricsConnection
from typing import Dict, Any

class Survey:
    def __init__(self, name:str):
        self._questions = []
        self._name = name
    
    def pushToQualtrics(self, qualtrics:QualtricsConnection): #TODO: confirm using OAuth vs other approaches?
        print(f"Yep, totally pushing survey {self._name} to Qualtrics right now.") #TODO: modify Prof. Butner's sample code to push to personal test survey
        return
    
    def addQuestion(self, question:Question):
        self._questions.append(question)
    
    # def generate_json(self) -> Dict[str, Any]:
    #     pass