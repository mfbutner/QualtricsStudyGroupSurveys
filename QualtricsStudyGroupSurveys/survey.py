from .question import Question
from .qualtrics_connection import QualtricsConnection
from typing import Dict, Any

class Survey:
    def __init__(self, name:str, id:str):
        self._questions = []
        self._name = name
        self._id = id
        # self._header = {
        #     "id" : "Manually Removed Due To Being publiclly hosted",
        #     "name": self._name,
        #     "ownerID": "Manually Removed Due To Being publiclly hosted",
        #     "organizationId": "ucdavis",
        #     "isActive": True,
        #     "creationDate": "2025-08-01T23:40:20Z",
        #     "lastModifiedDate": "2025-08-21T23:02:47Z",
        #     "expiration": {
        #         "startDate": None,
        #         "endDate": None
        #     }
        # }
    
    def pushToQualtrics(self, qualtrics:QualtricsConnection) -> str: # TODO: Push flow, blocks as well so that the survey is formatted properly
        response = ""
        for (i, question) in enumerate(self._questions):
            response += qualtrics.add_question(self._id, f"QID{i + 1}", question) + '\n'
        return response
    
    def addQuestion(self, question:Question):
        self._questions.append(question)
    
    def generate_json(self) -> Dict[str, Any]:
        return {
            "elements": [question.generate_json(f"QID{i + 1}") for (i,question) in enumerate(self._questions)]
        }
        # output = self._header
        # self._header["questions"] = {f"QID{i + 1}": question.generate_json() for (i, question) in enumerate(self._questions)}
        # return output