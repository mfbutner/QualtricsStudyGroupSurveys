from question import Question

class Survey:
    def __init__(self, name:str):
        self._questions = []
        self._name = name
    
    def pushToQualtrics(self, client_ID:str, client_secret:str):
        return
    
    def addQuestion(self, question:Question):
        self._questions.append(Question)