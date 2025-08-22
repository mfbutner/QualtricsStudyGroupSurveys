from .question import Question
from .qualtrics_connection import QualtricsConnection
from typing import Dict, Any

class Survey:
    def __init__(self, name:str):
        self._questions = []
        self._name = name
        self._header = {
            "id" : "Manually Removed Due To Being publiclly hosted",
            "name": self._name,
            "ownerID": "Manually Removed Due To Being publiclly hosted",
            "organizationId": "ucdavis",
            "isActive": "true",
            "creationDate": "2025-08-01T23:40:20Z",
            "lastModifiedDate": "2025-08-21T23:02:47Z",
            "expiration": {
                "startDate": "null",
                "endDate": "null"
            }
        }
    
    def pushToQualtrics(self, qualtrics:QualtricsConnection): #TODO: confirm using OAuth vs other approaches?
        print(f"Yep, totally pushing survey {self._name} to Qualtrics right now.") #TODO: modify Prof. Butner's sample code to push to personal test survey
        return
    
    def addQuestion(self, question:Question):
        self._questions.append(question)
    
    def generate_json(self) -> Dict[str, Any]:
        output = self._header
        output["questions"] = [question.generate_json() for question in self._questions]
        return output