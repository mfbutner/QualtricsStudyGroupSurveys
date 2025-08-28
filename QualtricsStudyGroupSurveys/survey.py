from typing import Dict, Any
from .question import Question
from .block import Block
from .qualtrics_connection import QualtricsConnection
from .flow import Flow, Root

import json
class Survey:
    def __init__(self, name:str, id:str, qualtrics:QualtricsConnection):
        self._questions = []
        self._blocks = []
        self._flows = []
        self._name = name
        self._id = id
        self._qualtrics = qualtrics
        
    def add_question(self, question:Question) -> str:
        response = self._qualtrics.create_question(self._id, question)
        question.set_ID(response['result']['QuestionID'])
        self._questions.append(question)
        return response['result']['QuestionID']
    
    def add_block(self, block:Block) -> str:
        response = self._qualtrics.create_block(self._id, block)
        return response['result']['BlockID']

    def add_flow(self, flow:Flow):
        self._flows.append(flow)
    
    def push_flows_to_qualtrics(self):
        all_flows = Root("FL_1", self._flows)
        self._qualtrics.update_flows(self._id, all_flows)
    
    def generate_json(self) -> Dict[str, Any]: # can be used for checking output on cmdline, but probably not sent to qualtrics itself.
        return {
            "elements": [question.generate_json() for question in self._questions],
            "blocks": [block.generate_json() for block in self._blocks],
        }
        